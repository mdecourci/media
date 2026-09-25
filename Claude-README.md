# NESO Media Intelligence — AI Agent Process Design

Design for the AI agent process behind a Media Intelligence application for NESO. Covers the pipeline that takes persisted media content (from RSS, Inoreader, and web crawlers) through AI-assisted filtering, stakeholder/sector/topic classification, and summary generation — plus the supporting stakeholder taxonomy and Postgres schema.

---

# Purpose

The AI agent sits between two things already in place: a content store holding raw items pulled in from RSS feeds, Inoreader, and web crawlers, and the people who need insight from it — NESO teams tracking sentiment and activity across sectors and stakeholders. The agent's job is to turn a stream of raw articles into a small number of ranked, tagged, summarised items that map directly onto NESO's stakeholder taxonomy, so a user can filter by sector and immediately see what matters, rather than reading everything that was scraped that day.

It runs as two sequential LLM stages — a cheap classification pass and a more expensive summarisation pass — separated by a deduplication step, coordinated by a database-driven queue rather than a message broker.

# Two classification axes

Content is tagged along two independent axes:

- **Who** — the stakeholder taxonomy: stakeholder category → sector → organisation type → example organisations → keywords.
- **What** — a flat **topic** taxonomy (Clean Power 2030, flexibility markets, constraint costs, grid connections reform, whole-system planning, RESP) describing subject matter regardless of which stakeholder is involved.

An article can sit at "Network Operator → Electricity Distribution → DNO → SSEN" on one axis and "grid connection reform" on the other — both are needed for the dashboard to be genuinely filterable.

# What the agent does

**Filters for relevance.** Most crawled content has nothing to do with NESO or the energy sector. The first step decides, per item, whether it merits further processing, before the expensive summarisation stage runs.

**Classifies against the stakeholder taxonomy.** For relevant items, the agent assigns sectors, identifies stakeholder organisations, and extracts named entities (programmes, policies). The taxonomy lives in the database, not the prompt code, so adding a stakeholder is a data change, not a deployment.

**Deduplicates and clusters.** The same story often appears across multiple sources. Before summarising, the agent groups near-duplicate articles into a single cluster using embedding similarity, so users see one story once, backed by all its sources.

**Summarises and scores.** For each surviving cluster, a second LLM call produces a short neutral summary, sentiment toward NESO specifically, and an impact/priority score against NESO's known strategic priorities.

**Writes structured insight, not prose.** Every output is structured data — sector codes, stakeholder IDs, sentiment, score, summary text — persisted to an insights table that dashboards and alerts query directly.

# AI-assisted filtering

Filtering is a tiered gate, designed to keep the expensive LLM summarisation call from running on content that isn't worth it, while still catching genuinely relevant stories that don't obviously look relevant on the surface.

## Tier 1: cheap pre-filter, no LLM involved

A lightweight pass narrows the pool using keyword/entity matching against `taxonomy_keyword` rows, or a cheap embedding similarity check. Its only job is to drop content with zero plausible connection to energy, so LLM cost isn't spent on obvious noise. Ambiguous cases pass through.

## Tier 2: LLM relevance filter

The classification agent reads the article and returns a `relevant` boolean plus a `confidence` score:

- **High confidence relevant** → proceeds to clustering and summarisation.
- **High confidence not relevant** → discarded, no further cost incurred.
- **Low confidence, either direction** → routed to a human review queue rather than auto-decided, since silently dropping a real story is worse than a ten-second human check.

## Tier 3: human review queue

Borderline items (e.g. confidence 0.4–0.6) sit in a small review queue. A reviewer's decision resolves that item and becomes a labelled example for periodically checking whether the model's threshold is well-calibrated — if the queue consistently overturns the model in one direction, that signals a threshold or prompt adjustment, not just a one-off correction.

# Classify and tag content

The classification call returns codes, not free text — `sector_ids`, `organisation_ids`, `topic_ids` — validated against the taxonomy tables before insert, so a hallucinated sector or organisation is rejected rather than silently persisted. Enum lists (sectors, organisation types, topics) are generated from the database at call time, so the model reasons against the same vocabulary the data model stores.

# Generate summaries

The summarisation call runs only on relevant, deduplicated clusters, and receives the cluster's already-resolved tags (sector, organisation, topic labels) as context alongside the article text — so the summary is written with awareness of why the story matters, rather than the model re-deriving relevance from scratch.

# Orchestration: status-column polling instead of Kafka

Throughput here is bounded by ingestion rate and LLM latency, not high-volume streaming, so a polling worker with row-level locking handles coordination cleanly without an extra broker to operate.

```sql
ALTER TABLE content_item
  ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'new',
  ADD COLUMN retry_count INT NOT NULL DEFAULT 0,
  ADD COLUMN locked_at TIMESTAMP,
  ADD COLUMN updated_at TIMESTAMP NOT NULL DEFAULT now();

CREATE INDEX idx_content_item_status
  ON content_item(status) WHERE status IN ('new','classified');
```

Poller query — the piece that replaces a message queue:

```sql
SELECT * FROM content_item
WHERE status = 'new'
ORDER BY created_at
LIMIT :batchSize
FOR UPDATE SKIP LOCKED;
```

`SKIP LOCKED` lets multiple pod replicas poll concurrently without fighting over rows or needing a coordinator. Failure handling mirrors a dead-letter queue as data: increment `retry_count` on error, flip to `failed` past a threshold — a status you can query and dashboard rather than a separate queue to inspect. A stale `locked_at` gets swept back to `new`, covering a worker crashing mid-item.

If this outgrows a single database, Amazon SQS (already on AWS) is the natural next step rather than Kafka — visibility timeouts play the role of `locked_at`, with a native DLQ.

# Postgres schema

## Stakeholder taxonomy

```sql
CREATE TABLE stakeholder_category (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    label VARCHAR(150) NOT NULL,
    description TEXT
);

CREATE TABLE sector (
    id SERIAL PRIMARY KEY,
    stakeholder_category_id INT NOT NULL REFERENCES stakeholder_category(id),
    code VARCHAR(50) NOT NULL,
    label VARCHAR(150) NOT NULL,
    UNIQUE (stakeholder_category_id, code)
);

CREATE TABLE organisation_type (
    id SERIAL PRIMARY KEY,
    sector_id INT NOT NULL REFERENCES sector(id),
    code VARCHAR(50) NOT NULL,
    label VARCHAR(150) NOT NULL,
    UNIQUE (sector_id, code)
);

CREATE TABLE organisation (
    id SERIAL PRIMARY KEY,
    organisation_type_id INT NOT NULL REFERENCES organisation_type(id),
    name VARCHAR(200) NOT NULL,
    aliases TEXT[] DEFAULT '{}',
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE taxonomy_keyword (
    id SERIAL PRIMARY KEY,
    stakeholder_category_id INT REFERENCES stakeholder_category(id),
    sector_id INT REFERENCES sector(id),
    organisation_type_id INT REFERENCES organisation_type(id),
    organisation_id INT REFERENCES organisation(id),
    keyword VARCHAR(200) NOT NULL,
    weight NUMERIC(3,2) DEFAULT 1.0,
    CHECK (num_nonnulls(stakeholder_category_id, sector_id,
                         organisation_type_id, organisation_id) = 1)
);
```

## Topic taxonomy

```sql
CREATE TABLE topic (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    label VARCHAR(150) NOT NULL,
    description TEXT,
    keywords TEXT[] DEFAULT '{}'
);
```

## Content processing

```sql
CREATE TABLE content_item (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source VARCHAR(50) NOT NULL,
  source_url TEXT NOT NULL,
  title TEXT,
  body TEXT,
  published_at TIMESTAMPTZ,
  ingested_at TIMESTAMPTZ DEFAULT now(),
  status VARCHAR(20) NOT NULL DEFAULT 'new',
  retry_count INT DEFAULT 0,
  locked_at TIMESTAMPTZ,
  UNIQUE (source_url, published_at)
);

CREATE TABLE content_classification (
  id SERIAL PRIMARY KEY,
  content_item_id UUID REFERENCES content_item(id),
  relevant BOOLEAN NOT NULL,
  confidence NUMERIC(4,3) NOT NULL,
  sector_ids INT[],
  organisation_ids INT[],
  topic_ids INT[],
  reason TEXT,
  classified_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE content_cluster (
  id SERIAL PRIMARY KEY,
  representative_content_item_id UUID REFERENCES content_item(id),
  member_content_item_ids UUID[],
  embedding VECTOR(1536),
  status VARCHAR(20) DEFAULT 'open',
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE insight (
  id SERIAL PRIMARY KEY,
  content_cluster_id INT REFERENCES content_cluster(id),
  summary TEXT NOT NULL,
  sentiment VARCHAR(20),
  impact_score INT,
  priority_theme VARCHAR(150),
  sector_ids INT[],
  organisation_ids INT[],
  topic_ids INT[],
  generated_at TIMESTAMPTZ DEFAULT now()
);
```

# Example taxonomy records (JSON)

```json
{
  "stakeholder_category": { "code": "network_operator", "label": "Network Operator" },
  "sector": { "code": "electricity_distribution", "label": "Electricity Distribution" },
  "organisation_type": { "code": "dno", "label": "Distribution Network Operator (DNO)" },
  "examples": ["SSEN", "UK Power Networks", "Northern Powergrid",
               "National Grid Electricity Distribution"],
  "keywords": ["DNO", "distribution network operator",
               "grid connection queue", "DSO transition"]
}
```

```json
{
  "stakeholder_category": { "code": "generator", "label": "Generator" },
  "sector": { "code": "renewables", "label": "Renewables" },
  "organisation_type": { "code": "generator_renewable", "label": "Renewable Generator" },
  "examples": ["Drax", "SSE Renewables", "Orsted"],
  "keywords": ["offshore wind", "renewable generation", "CfD", "curtailment"]
}
```

```json
{
  "topic": {
    "code": "clean_power_2030",
    "label": "Clean Power 2030",
    "keywords": ["CP30", "2030 clean power target", "decarbonisation deadline"]
  }
}
```

# Content-processing data records (JSON)

**`content_item`** — the raw ingested article:

```json
{
  "id": "b3f1...uuid",
  "source": "rss",
  "source_url": "https://example.com/article",
  "title": "SSEN announces grid upgrade for Scottish connections",
  "body": "...",
  "published_at": "2026-09-20T09:15:00Z",
  "status": "new",
  "retry_count": 0
}
```

**`content_classification`** — output of the filtering + tagging stage:

```json
{
  "content_item_id": "b3f1...uuid",
  "relevant": true,
  "confidence": 0.91,
  "sector_ids": [4],
  "organisation_ids": [12],
  "topic_ids": [7],
  "reason": "Article discusses SSEN's connection queue reform, directly relevant to network operator sector"
}
```

**`content_cluster`** — deduplicated group feeding one summary:

```json
{
  "id": 501,
  "member_content_item_ids": ["b3f1...", "a92c...", "77de..."],
  "status": "summarized"
}
```

**`insight`** — final tagged, summarised output the dashboard reads:

```json
{
  "content_cluster_id": 501,
  "summary": "SSEN outlined a package of grid upgrades intended to reduce connection queue times for Scottish renewable projects.",
  "sentiment": "positive",
  "impact_score": 4,
  "priority_theme": "grid connections reform",
  "sector_ids": [4],
  "organisation_ids": [12],
  "topic_ids": [7]
}
```

# Prompts

Both calls use structured/tool-calling output rather than free-form text. Enum lists are interpolated from the database at call time.

## Classification prompt

**System:**

> You are a media analyst for the National Energy System Operator (NESO). Your job is to read a single article and decide whether it is relevant to NESO, the GB energy system, or any of NESO's tracked stakeholders, and if so, tag it against NESO's sector, organisation, and topic taxonomy. Only mark an article relevant if it concerns UK/GB energy system operation, planning, policy, or a named stakeholder — general international energy news with no GB relevance should be marked not relevant. Do not invent sectors, organisations, or topics outside the provided lists. If uncertain, prefer a lower confidence score over guessing.
>
> Sectors: {{sector_list_with_descriptions}}
> Known organisations: {{organisation_list_with_type}}
> Topics: {{topic_list_with_descriptions}}

**User:**

> Article title: {{title}}
> Source: {{source}}
> Published: {{published_date}}
> Body:
> {{article_body}}
>
> Classify this article using the classify_article tool.

**Tool schema:**

```json
{
  "name": "classify_article",
  "input_schema": {
    "type": "object",
    "properties": {
      "relevant": { "type": "boolean" },
      "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
      "sector_codes": { "type": "array", "items": { "type": "string" } },
      "organisation_names": { "type": "array", "items": { "type": "string" } },
      "topic_codes": { "type": "array", "items": { "type": "string" } },
      "reason": { "type": "string" }
    },
    "required": ["relevant", "confidence", "sector_codes",
                 "organisation_names", "topic_codes"]
  }
}
```

## Summarisation prompt

**System:**

> You are a media analyst producing a briefing summary for NESO leadership. You will be given one or more articles reporting the same underlying story, plus its sector, organisation, and topic tags. Write a single neutral summary that synthesises all sources rather than favouring one. Assess sentiment specifically as it reflects on NESO, not the general tone of the article. Score impact based on relevance to NESO's known strategic priorities: demand-side flexibility, whole-system scope (gas, electricity, heat), constraint costs, and Clean Power 2030 delivery. Do not speculate beyond what the sources state.

**User:**

> Story cluster ({{n}} sources):
> {{concatenated_article_excerpts_with_source_labels}}
>
> Sectors involved: {{sectors_from_classification}}
> Organisations involved: {{organisations_from_classification}}
> Topics involved: {{topics_from_classification}}
>
> Summarise this cluster using the summarize_cluster tool.

**Tool schema:**

```json
{
  "name": "summarize_cluster",
  "input_schema": {
    "type": "object",
    "properties": {
      "summary": { "type": "string" },
      "sentiment": { "type": "string", "enum": ["positive", "neutral", "negative"] },
      "impact_score": { "type": "integer", "minimum": 1, "maximum": 5 },
      "priority_theme": { "type": "string" }
    },
    "required": ["summary", "sentiment", "impact_score"]
  }
}
```

Set temperature to 0 on both calls and pin the model version — this matters more for classification consistency over time than for summarisation wording.
