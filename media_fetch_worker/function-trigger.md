
### This is an Azure Functions timer-triggered Python fetch worker for Stage 1 (Discovery & Fetch) of the Media Intelligence pipeline:

**function_app.py** 
- runs on a schedule (0 0 6,12,18 * * *, matching the 2–3x/day 06:00–18:00 cadence)
- loops over a list of RSS feeds (each tagged with a keyword_set from Section 0's tag tables), parses entries with feedparser, 
- builds a Raw Store-shaped record (source, publish date, fetch timestamp, raw text, content hash), and writes each as an immutable JSON blob to Azure Blob Storage 
- deduplicating via content hash so re-runs don't rewrite the same item.

**Implementation**
- Auth: uses BlobServiceClient.from_connection_string(...) only — no azure-identity, no DefaultAzureCredential, no managed identity. The connection string comes from the 
  AZURE_STORAGE_CONNECTION_STRING app setting. 
- requirements.txt — azure-functions, azure-storage-blob, feedparser. 
- host.json — standard Functions v4 host config. 
- local.settings.json.example — shows the expected app settings, including the feed-to-keyword_set mapping (FEED_CONFIG_JSON) — copy to local.settings.json and fill in real values for local runs; never commit real keys.

Blob naming follows 
```json
<keyword_set>/<yyyy>/<mm>/<dd>/<content_hash>.json
```
so items land already partitioned by topic and date, ready for Stage 2 (filtering) to pick up.

For this fetch worker, you need a fairly small set of resources — no Entra ID / managed identity setup required since it's connection-string based.

## Required Azure resources

| Resource | Purpose |
|---|---|
| **Resource Group** | Container for everything below. |
| **Storage Account** | Two roles: (1) the Function App's own internal storage (`AzureWebJobsStorage` — timer trigger locks, logs), (2) hosts the `media-raw-store` blob container the worker writes to. Can be one account or split into two — one account is fine for dev/test. |
| **Blob container** (`media-raw-store`) | Created inside the storage account — the code auto-creates it on first run if missing, but you can pre-create it. |
| **Function App** | Hosts and runs `function_app1.py` on the timer trigger. Needs a Python 3.10/3.11 runtime stack. |
| **App Service Plan / hosting plan** | Backs the Function App. Consumption (Y1) plan is the cheapest fit for a scheduled fetch job; Premium (EP1) if you need longer execution time, VNet integration, or no cold starts. |
| **Application Insights** *(recommended, not strictly required)* | Captures the `logging.info`/`logging.exception` calls in the code so you can see run history and failures. |

## What you don't need
- No Entra ID app registration.
- No managed identity assignment on the Function App.
- No RBAC role assignment on the storage account (e.g. "Storage Blob Data Contributor") — access is entirely via the connection string in app settings.

## Minimal `az cli` setup

```bash
# Variables
RG = rg-media-intel
LOCATION = uksouth
STORAGE = stmediaintel$RANDOM   # storage account names must be globally unique
FUNCAPP = func-media-fetch-worker
PLAN = plan-media-fetch-worker

# 1. Resource group
az group create -n $RG -l $LOCATION

# 2. Storage account (used for both AzureWebJobsStorage and the raw store container)
az storage account create -n $STORAGE -g $RG -l $LOCATION --sku Standard_LRS

# 3. Blob container for raw content
az storage container create --account-name $STORAGE -n media-raw-store

# 4. Consumption hosting plan
az functionapp plan create -g $RG -n $PLAN --location $LOCATION --sku Y1 --is-linux

# 5. Function App (Python)
az functionapp create -g $RG -n $FUNCAPP --plan $PLAN \
  --storage-account $STORAGE --runtime python --runtime-version 3.11 \
  --functions-version 4 --os-type Linux

# 6. App settings — connection string based, no identity
CONN_STR=$(az storage account show-connection-string -n $STORAGE -g $RG -o tsv)
az functionapp config appsettings set -g $RG -n $FUNCAPP --settings \
  "AZURE_STORAGE_CONNECTION_STRING=$CONN_STR" \
  "RAW_CONTAINER_NAME=media-raw-store" \
  'FEED_CONFIG_JSON=[{"keyword_set":"clean_power_2030","source_name":"BBC Energy","feed_url":"https://example.com/rss"}]'
```
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=stmediaintel;AccountKey=txLaXsnG9X1dhOIWlub7AIhTqi06OKLTITSA8W2htyPrPxnynuIArAmlT4Eq9bVNRhxJnqAf6uXF+AStNO4bgw==;EndpointSuffix=core.windows.net

Then deploy the code with `func azure functionapp publish $FUNCAPP` (from the `media_fetch_worker` folder, with the Azure Functions Core Tools installed).

One thing worth flagging: a storage account connection string carries the full account key, so treat it like a secret — Azure Key Vault (referenced via `@Microsoft.KeyVault(...)` in app settings) is a common middle ground that keeps you off Entra ID auth for the blob calls themselves while not storing the raw key directly in Function App settings.