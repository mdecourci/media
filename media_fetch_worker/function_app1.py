"""
Media Intelligence - Fetch Worker (Stage 1: Discovery & Fetch)
================================================================

Azure Function, triggered on a schedule, that:
  1. Reads a set of RSS/media feed URLs (one "keyword_set" per feed) from
     configuration.
  2. Fetches each feed.
  3. Writes each retrieved item as an immutable JSON blob to Azure Blob
     Storage, matching the Raw Store record shape used by the Media
     Intelligence pipeline (source_url, source_name, publish_date,
     fetch_timestamp, raw_text, content_hash, keyword_set).

AUTHENTICATION NOTE
--------------------
This function intentionally does NOT use Entra ID / Azure AD / managed
identity (i.e. no DefaultAzureCredential, no azure-identity package).
It authenticates to Blob Storage purely with a storage account
connection string, supplied via the app setting
AZURE_STORAGE_CONNECTION_STRING (see local.settings.json.example).
"""

import hashlib
import json
import logging
import os
from datetime import datetime, timezone

import azure.functions as func
import feedparser  # type: ignore[import-untyped]
from azure.functions import TimerRequest
from azure.storage.blob import BlobServiceClient, ContentSettings

app = func.FunctionApp()

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

# Connection-string based auth only - no Entra ID / managed identity.
STORAGE_CONNECTION_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
RAW_CONTAINER_NAME = os.environ.get("RAW_CONTAINER_NAME", "media-raw-store")

# Each entry maps a keyword_set (as defined in the pipeline DDL) to the feed
# it should be fetched from. In production this could instead be loaded
# from a config blob/table rather than an environment variable.
#
# Expected JSON shape (env var FEED_CONFIG_JSON):
# [
#   {"keyword_set": "clean_power_2030", "source_name": "BBC Energy", "feed_url": "https://.../rss"},
#   {"keyword_set": "scottish_power_networks", "source_name": "Utility Week", "feed_url": "https://.../rss"}
# ]
FEED_CONFIG: list[dict] = json.loads(z)


@app.timer_trigger(
    schedule="*/10 * 0 * * ?",
    arg_name="fetchTimer",
    run_on_startup=False,
    use_monitor=True,
)
def media_fetch_worker(fetchTimer: func.TimerRequest) -> None:
    logging.info("media_fetch_worker: starting")
    x = os.environ.get("FEED_CONFIG_JSON").encode()  # type: ignore
    z = "[{\"keyword_set\": \"clean_power_2030\", \"source_name\": \"BBC Energy\", \"feed_url\": \"https://example.com/energy/rss\"}, {\"keyword_set\": \"scottish_power_networks\", \"source_name\": \"Utility Week\", \"feed_url\": \"https://example.com/utility-week/rss\"}]"
    FEED_CONFIG = json.loads(z)
    if fetchTimer.past_due:
        logging.warning("media_fetch_worker: timer trigger is running late.")

    logging.info("media_fetch_worker: starting run for %d feed(s).", len(FEED_CONFIG))

    blob_service_client = BlobServiceClient.from_connection_string(
        STORAGE_CONNECTION_STRING
    )
    container_client = get_or_create_container(blob_service_client, RAW_CONTAINER_NAME)
    logging.info("media_fetch_worker: created container %s.", RAW_CONTAINER_NAME)

    total_written = 0
    logging.info("media_fetch_worker: FEED_CONFIG")

    for feed_cfg in FEED_CONFIG:
        keyword_set = feed_cfg.get("keyword_set", "unknown")
        source_name = feed_cfg.get("source_name", "unknown")
        feed_url = feed_cfg.get("feed_url")

        if not feed_url:
            logging.warning("Skipping feed config with no feed_url: %s", feed_cfg)
            continue

        try:
            written = _fetch_and_store_feed(
                container_client=container_client,
                keyword_set=keyword_set,
                source_name=source_name,
                feed_url=feed_url,
            )
            total_written += written
        except Exception as exc:  # noqa: BLE001 - log and continue with next feed
            logging.exception(
                "media_fetch_worker: failed to process feed '%s' (%s): %s",
                keyword_set,
                feed_url,
                exc,
            )

    logging.info("media_fetch_worker: run complete. %d item(s) written.", total_written)


def get_or_create_container(blob_service_client: BlobServiceClient, container_name):
    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.create_container()
        logging.info("Created container '%s'.", container_name)
    except Exception:
        # Container already exists - safe to ignore.
        pass
    return container_client

if __name__ == "__main__":
    fetchTimer: TimerRequest = func.TimerRequest()
    media_fetch_worker(fetchTimer)


def _fetch_and_store_feed(  # type: ignore[no-untyped-def]
        container_client,
        keyword_set: str,
        source_name: str,
        feed_url: str,
) -> int:
    """Fetch a single RSS/Atom feed and write each entry as a raw blob.

    Returns the number of items written.
    """
    parsed = feedparser.parse(feed_url)

    if parsed.bozo:
        logging.warning(
            "Feed '%s' (%s) parsed with warnings: %s", keyword_set, feed_url, parsed.bozo_exception
        )

    written = 0
    for entry in parsed.entries:
        raw_record = _build_raw_record(entry, keyword_set, source_name, feed_url)
        blob_name = _blob_name_for(raw_record)

        if _blob_exists(container_client, blob_name):
            # content_hash already present -> duplicate/previously fetched item.
            continue

        container_client.upload_blob(
            name=blob_name,
            data=json.dumps(raw_record, ensure_ascii=False, indent=2),
            overwrite=False,
            content_settings=ContentSettings(content_type="application/json"),
        )
        written += 1

    logging.info(
        "Feed '%s' (%s): %d new item(s) written to blob storage.",
        keyword_set,
        feed_url,
        written,
    )
    return written


def _build_raw_record(entry, keyword_set: str, source_name: str, feed_url: str) -> dict:  # type: ignore[type-arg,no-untyped-def]
    """Builds a Raw Store-shaped record from a parsed feed entry."""
    source_url = getattr(entry, "link", "")
    raw_text = _extract_text(entry)
    publish_date = _extract_publish_date(entry)
    fetch_timestamp = datetime.now(timezone.utc).isoformat()
    content_hash = hashlib.sha256(
        f"{source_url}|{raw_text}".encode("utf-8")
    ).hexdigest()

    return {
        "keyword_set": keyword_set,
        "source_name": source_name,
        "source_url": source_url,
        "publish_date": publish_date,
        "fetch_timestamp": fetch_timestamp,
        "raw_text": raw_text,
        "content_hash": content_hash,
    }


def _extract_text(entry) -> str:  # type: ignore[no-untyped-def]
    title = getattr(entry, "title", "")
    summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
    return f"{title}\n\n{summary}".strip()


def _extract_publish_date(entry) -> str:  # type: ignore[no-untyped-def]
    published_parsed = getattr(entry, "published_parsed", None)
    if published_parsed:
        return datetime(*published_parsed[:6], tzinfo=timezone.utc).isoformat()  # type: ignore[misc]
    return ""


def _blob_name_for(raw_record: dict) -> str:  # type: ignore[type-arg]
    """Deterministic blob path: <keyword_set>/<yyyy>/<mm>/<dd>/<content_hash>.json"""
    fetched_at = datetime.fromisoformat(raw_record["fetch_timestamp"])
    return (
        f"{raw_record['keyword_set']}/"
        f"{fetched_at:%Y/%m/%d}/"
        f"{raw_record['content_hash']}.json"
    )


def _blob_exists(container_client, blob_name: str) -> bool:  # type: ignore[no-untyped-def]
    blob_client = container_client.get_blob_client(blob_name)
    return blob_client.exists()  # type: ignore[no-any-return]
