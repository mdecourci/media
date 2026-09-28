# chatgpt-dld.md
# Media Intelligence Component – Detailed Design

## 1. Scope and assumptions

**Scope:**
- Detailed design of the Media Intelligence Component (MIC) that:
  - Ingests external media/news.
  - Applies AI‑assisted filtering.
  - Classifies and tags content.
  - Generates AI summaries.
  - Exposes enriched outputs via APIs and events.
- Designed to support NESO’s insight, planning, and operational teams.

**Key assumptions:**
- Event‑driven, microservice‑oriented architecture.
- Cloud‑hosted (vendor‑agnostic; examples use common managed services).
- LLM access via a model gateway (could be external or on‑prem).
- No semantic requirements imposed on external clients.

---

## 2. Logical architecture

### 2.1 Services

- **Source Registry & Scheduler**
- **Ingestion Service**
- **Pre‑processing Service**
- **AI Filtering Service**
- **Classification & Tagging Service**
- **Summarisation Service**
- **Content Store & Index Service**
- **API Gateway & Query Service**
- **Event Publisher**
- **Configuration Service**
- **Observability Stack**

### 2.2 Data stores

- **Config DB** – source registry, profiles, taxonomies, templates.
- **Raw Content Store** – raw articles/documents.
- **Enriched Content Store** – enriched items + summaries.
- **Search Index** – full‑text + metadata.
- **Vector Store (internal)** – embeddings for internal semantic search.
- **Metrics & Logs Store** – observability.

---

## 3. Data model

### 3.1 Core entities

#### 3.1.1 Source
```json
{
  "id": "src-bbc-energy",
  "name": "BBC Energy",
  "type": "rss",          // rss | api | crawler
  "endpoint": "https://example.com/rss",
  "poll_interval_sec": 300,
  "language": "en",
  "region": "GB",
  "enabled": true,
  "tags": ["media", "news", "energy"]
}
```

## 4. Component detailed design
## 4.1 Source Registry & Scheduler

- Responsibilities:
  - Maintain list of sources and polling intervals.
  - Trigger ingestion jobs.

- Implementation:
  - Config DB (e.g., PostgreSQL).
  - Scheduler (e.g., cron‑like service or managed scheduler).
  - REST admin API:
	- POST /sources
	- PUT /sources/{id}
	- GET /sources
**Key logic:**
- For each enabled source:
  - Ceate job with source_id, endpoint, poll_interval_sec.
  - Emt IngestionJobRequested event to message bus.

## 4.2 Ingestion Service
- Responsibilities:
  - Execute ingestion jobs.
  - Fetch raw content.
  - Persist RawNewsItem.
- Interfaces:
  - Consumes IngestionJobRequested events.
  - Publishes RawNewsItemCreated events.

- Processing steps:
  1. Receive job.
  2. Fetch data:
     - RS: parse XML.
	 - API: call JSON endpoint.
	 - Crawler: run scraping pipeline.
  3. For each article:
	 - Build RawNewsItem.
     - Compute content_hash for dedup.
	 - Store in Raw Content Store.
	 - Publish RawNewsItemCreated.
- Error handling:
- Retry with exponential backoff on network errors.
- Circuit breaker per source.
- Log failures with source ID and endpoint.

## 4.3 Pre‑processing Service
- Responsibilities:
  - Convert RawNewsItem to NewsDocument.
  - Clean text, deduplicate, validate.
- Interfaces:
  - Consumes RawNewsItemCreated.
  - Publishes NewsDocumentReady.
- Processing steps:
  - Load raw item. 
  - Clean:
    - Stip HTML.
	- Remove navigation/ads via boilerplate removal.
  - Detect language (if missing).
  - Validate:
	- Minimum length.
	- Supported language.
  - Deduplicate:
	- Check content_hash or similarity against recent docs. 
  - Persist NewsDocument.
  - Publish NewsDocumentReady.

## 4.4 AI Filtering Service
- Responsibilities:
  - Apply AI‑assisted relevance scoring.
  - Produce FilterDecision.
- Interfaces:
  - Consumes NewsDocumentReady.
  - Publishes FilterDecisionMade.
- Configuration:
  - Profiles stored in Config DB:
  
{
  "id": "neso-default",
  "name": "NESO Default Profile",
  "min_relevance": 0.7,
  "blocked_topics": ["sports"],
  "priority_topics": ["energy", "policy", "infrastructure"]
}

Processing steps:
1. Load NewsDocument and profile.
2. Rule‑based pre‑filter:
	◦ If topic clearly blocked → decision = discard.
3. AI scoring:
	◦ Call classifier: score = relevance(doc, profile).
	◦ Optionally call LLM scoring for borderline cases.
4. Decision:
	◦ score >= min_relevance → accept.
	◦ score >= (min_relevance - 0.1) → deprioritise.
	◦ Else → discard.
5. Persist FilterDecision.
6. If accept or deprioritise, publish DocumentAcceptedForEnrichment.
---
4.5 Classification & Tagging Service
Responsibilities:
• Classify topics.
• Extract entities.
• Generate tags.
Interfaces:
• Consumes DocumentAcceptedForEnrichment.
• Publishes EnrichedNewsItemCreated.
Taxonomy:
• Stored in Config DB:
{
  "version": "tax-v2.0",
  "domains": ["Electricity", "Gas", "Whole System"],
  "topics": ["Decarbonisation", "Security of Supply", "Market Design"],
  "entity_types": ["organisation", "location", "technology"]
}

Processing steps:
1. Load NewsDocument and taxonomy.
2. Topic classification:
	◦ Use ML model to assign topics (multi‑label).
3. NER:
	◦ Extract entities (orgs, locations, technologies).
	◦ Map to canonical IDs via entity registry.
4. Tag generation:
	◦ Combine topics, entities, keywords into tags.
5. Sentiment (optional).
6. Build EnrichedNewsItem.
7. Persist to Enriched Content Store.
8. Publish EnrichedNewsItemCreated.
---
4.6 Summarisation Service (AI Agent)
Responsibilities:
• Generate summaries for each enriched item.
• Support multiple summary types.
Interfaces:
• Consumes EnrichedNewsItemCreated.
• Publishes SummaryGenerated.
Templates:
• Stored in Config DB:

{
  "id": "tmpl-exec-v1",
  "type": "executive",
  "language": "en",
  "system_prompt": "You are an energy system analyst writing concise executive summaries.",
  "style_guidelines": [
    "Neutral tone",
    "No speculation",
    "Focus on GB energy system implications"
  ],
  "max_tokens": 200
}

Processing steps:
1. Load EnrichedNewsItem.
2. For each required summary type (short, analyst, executive):
	◦ Select template.
	◦ Build prompt:
		▪︎ System prompt + content + metadata (topics, entities).
	◦ Call model gateway.
	◦ Validate:
		▪︎ Length within limits.
		▪︎ Language matches.
	◦ Persist Summary.
	◦ Publish SummaryGenerated.
Caching:
• Cache summaries keyed by enriched_id + type + template_version.
---
4.7 Content Store & Index Service
Responsibilities:
• Persist raw, canonical, enriched, and summary data.
• Maintain search and vector indices.
Implementation:
• Raw Content Store: object storage (e.g., S3‑like).
• Enriched Content Store: document DB (e.g., MongoDB).
• Search Index: search engine (e.g., OpenSearch/Elastic).
• Vector Store: embeddings DB (internal).
Indexing pipeline:
1. On EnrichedNewsItemCreated or SummaryGenerated:
	◦ Build index document:

{
  "id": "enr-20260927-001",
  "title": "...",
  "body": "...",
  "tags": ["renewables", "offshore-wind"],
  "topics": ["Decarbonisation"],
  "entities": ["NESO", "North Sea"],
  "relevance_score": 0.87,
  "published_at": "2026-09-27T11:00:00Z",
  "source_id": "src-bbc-energy"
}

• Index into search engine.
• Optionally compute embeddings and store in vector DB.
---
4.8 API Gateway & Query Service
Responsibilities:
• Expose query APIs.
• Handle authentication, rate limiting.
Endpoints:
GET /news
Query enriched items.
Query parameters:
• from, to
• source
• tags
• topics
• entities
• summary_type
• min_relevance
Flow:
1. Validate auth.
2. Build search query.
3. Query search index.
4. Fetch summaries (if requested).
5. Shape response.
GET /news/{id}
Retrieve single item with summaries.
GET /entities
List entities and their occurrences.
---
4.9 Event Publisher
Responsibilities:
• Publish events for downstream consumers (e.g., NESO dashboards, BI tools).
Events:
• EnrichedNewsItemCreated
• SummaryGenerated
• NewsItemUpdated (if re‑classified or re‑summarised)
Transport:
• Message bus (e.g., Kafka/EventHub).
---
4.10 Configuration Service
Responsibilities:
• Centralised configuration for:
	◦ Source registry.
	◦ Profiles.
	◦ Taxonomies.
	◦ Summary templates.
	◦ Model routing.
Interfaces:
• Admin UI + REST API.
• Versioning of configs.
---
4.11 Observability Stack
Responsibilities:
• Metrics, logs, traces.
Metrics examples:
• Ingestion rate per source.
• Average enrichment latency.
• Model error rate.
• Summary generation latency.
Logs:
• Per item pipeline trace (correlation ID).
• Error logs with stack traces.
Traces:
• Distributed tracing across services.
---
5. Sequence flows
5.1 Ingestion to enrichment
1. Scheduler emits IngestionJobRequested.
2. Ingestion Service fetches articles, stores RawNewsItem, emits RawNewsItemCreated.
3. Pre‑processing Service creates NewsDocument, emits NewsDocumentReady.
4. AI Filtering Service creates FilterDecision, emits DocumentAcceptedForEnrichment.
5. Classification & Tagging Service creates EnrichedNewsItem, emits EnrichedNewsItemCreated.
6. Summarisation Service creates Summary, emits SummaryGenerated.
7. Index Service updates search and vector indices.
---
5.2 Query path
1. Client calls GET /news.
2. API Gateway authenticates and authorises.
3. Query Service builds search query and hits search index.
4. Results enriched with summaries (if requested).
5. Response returned with pagination.
---
6. Error handling and resilience
• Network errors: retries with exponential backoff; per‑source circuit breakers.
• Model failures: fallback to simpler models or mark item for reprocessing.
• Index failures: queue index updates and retry; log and alert.
• Partial failures: pipeline continues where possible; items flagged with error status.
---
7. Security and governance
• AuthN/AuthZ: OAuth2/JWT for APIs; role‑based access for admin functions.
• Data protection: encryption at rest and in transit.
• Auditability:
	◦ Store model versions, prompts, and decisions.
	◦ Maintain change history for taxonomies and templates.
• Retention: configurable per source and region.
---
8. Deployment and scaling
• Containerised services (e.g., Kubernetes).
• Horizontal scaling:
	◦ Ingestion, pre‑processing, AI services, indexers.
• Autoscaling triggers:
	◦ Queue depth.
	◦ CPU/memory usage.
	◦ Latency thresholds.
---
9. Extensibility
• Add new sources via Source Registry.
• Add new profiles for different NESO teams.
• Extend taxonomy with new domains/topics.
• Introduce new summary types (e.g., “regulatory brief”, “market signal”).
---


