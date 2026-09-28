# Media Intelligence Component — High-Level Design

**System:** NESO Media Intelligence Component  
**Document status:** Draft HLD  
**Organisation:** National Energy System Operator (NESO)

---

## 1. Purpose

The **Media Intelligence Component (MIC)** provides NESO with an automated capability to discover, collect, process and analyse external media information relevant to NESO, its stakeholders, sectors and areas of strategic interest.

The component transforms potentially large volumes of external media content into structured, searchable and human-reviewed intelligence items.

### Primary capabilities

1. Fetch media information
2. AI-assisted filtering
3. Classify and tag content
4. Identify relevant stakeholders and sectors
5. Detect and assess sentiment
6. Generate article summaries
7. Provide traceability to the original source
8. Route AI-generated intelligence through human review
9. Publish approved intelligence for downstream analytics and reporting

The component is intended to operate as a reusable service rather than being tightly coupled to the Power BI dashboard.

---

## 2. NESO Business Context

NESO is responsible for planning and delivering the energy system of today and the future. Its role extends beyond electricity system operation to a whole-system view involving different forms of energy and relationships with other sectors.

NESO identifies eight major areas of activity:

- Energy Insights
- Strategic Planning
- Security of Supply
- Resilience & Emergency Management
- Energy Markets
- Systems Operations
- Connections
- Data & AI

The Data & AI capability is particularly relevant to this component. NESO's direction is to bring together data from multiple sources to support a digitalised energy system and use AI to generate insights and support evidence-based decisions.

NESO also operates in an environment involving a broad range of stakeholders, including government, Ofgem, energy industry participants, consumers and regional representatives. Its stakeholder engagement is intended to provide scrutiny, challenge, expertise and a whole-energy-system view.

This creates a business requirement to understand not only NESO's own communications but also how relevant external organisations, sectors and issues are being discussed in the wider media.

---

## 3. Business Need

The existing Strategic Intelligence Dashboard (SID) HLD identifies a requirement to:

> Continuously discover, normalise, and enrich media content about named stakeholders/sectors.

AI-generated sentiment and summaries are to be routed through a human-in-the-loop approval process before dashboard consumption.

The Media Intelligence Component provides the processing capability between external media sources and the Strategic Intelligence Dashboard.

### Business objectives

The component should enable NESO to:

- Maintain awareness of relevant external media.
- Identify articles relevant to NESO stakeholders and sectors.
- Reduce the volume of material requiring manual assessment.
- Identify emerging themes and issues.
- Understand the sentiment expressed in relevant content.
- Classify articles consistently.
- Provide concise summaries for human review.
- Retain links to original source material.
- Provide an auditable record of how AI-generated intelligence was produced.
- Ensure that only reviewed and approved intelligence reaches downstream reporting.

---

## 4. Scope

### 4.1 In scope

#### Media acquisition

- Scheduled retrieval of media content.
- RSS-based ingestion as the primary acquisition mechanism.
- Support for multiple approved media feeds.
- Capture of article metadata.
- Capture of article content where legally and technically permitted.
- Source URL preservation.
- Publication timestamp preservation.
- Source identification.

#### Content filtering

AI-assisted and rule-based filtering will determine whether an item is relevant to the configured monitoring scope.

Filtering may consider:

- NESO
- Named stakeholders
- Organisations
- Energy sectors
- Technologies
- Geographic areas
- Strategic topics
- Configurable keywords
- Combinations of topics and entities

#### Classification

Relevant content will be assigned one or more categories.

Examples include:

- NESO
- Electricity
- Gas
- Energy markets
- Network connections
- Renewable energy
- Clean power
- Energy security
- Infrastructure
- Regulation
- Government policy
- Consumer impact
- Communities
- Environment
- Technology / Data & AI

The classification taxonomy should remain configurable rather than being hard-coded into the application.

#### Entity identification

The system will identify entities appearing in content, for example:

- NESO
- Network operators
- Generators
- Government organisations
- Regulators
- Energy companies
- Consumer groups
- Community groups
- Technology organisations

#### Sentiment analysis

The system may generate:

- Sentiment label
- Sentiment score
- Confidence
- Supporting evidence
- Relevant text or article context

Sentiment should be treated as AI-generated analysis rather than an authoritative fact.

#### Summarisation

The AI service will generate a concise summary of relevant content.

The summary should preserve:

- Main subject
- Important facts
- Organisations involved
- Implications described by the source
- Relevant stakeholder or sector
- Source attribution

#### Human review

AI-generated results will be placed into a review queue.

The reviewer should be able to see:

- Original article information
- Source URL
- Article content available to the system
- AI classification
- Detected entities
- Sentiment
- AI summary
- Confidence
- Processing timestamp

The reviewer can:

- Approve
- Reject
- Request changes
- Add or modify tags
- Provide rationale

#### Publication

Only approved intelligence will be made available to downstream reporting and analytics.

---

## 5. Out of Scope

The following are outside the primary responsibility of MIC:

- Making operational decisions for NESO.
- Automatically publishing unreviewed AI-generated intelligence.
- Replacing human judgement.
- Making regulatory or policy decisions.
- Generating external communications automatically.
- Full social-media monitoring unless separately approved.
- Crawling unrestricted internet content.
- Circumventing paywalls, authentication or website access controls.
- Providing a general-purpose conversational AI interface.

---

## 6. High-Level Architecture

```text
                         ┌─────────────────────────┐
                         │ Approved Media Sources  │
                         │                         │
                         │ RSS feeds / APIs        │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Media Acquisition       │
                         │                         │
                         │ Scheduler               │
                         │ Feed retrieval          │
                         │ Source validation       │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Raw Media Store         │
                         │                         │
                         │ Article                 │
                         │ Metadata                │
                         │ Source URL              │
                         │ Retrieval timestamp     │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Normalisation           │
                         │                         │
                         │ Clean content           │
                         │ Canonical metadata      │
                         │ Content validation      │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Deduplication           │
                         │                         │
                         │ URL                     │
                         │ Content hash            │
                         │ Similarity               │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ AI Intelligence         │
                         │                         │
                         │ Relevance filtering     │
                         │ Classification          │
                         │ Entity extraction       │
                         │ Tagging                 │
                         │ Sentiment               │
                         │ Summarisation           │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Review Queue             │
                         │                         │
                         │ Human validation        │
                         │ Amend / reject / approve│
                         └────────────┬────────────┘
                                      │
                                Approved only
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Intelligence Store      │
                         │                         │
                         │ Approved articles       │
                         │ Tags                    │
                         │ Sentiment               │
                         │ Summaries               │
                         │ Audit information       │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Downstream Consumers    │
                         │                         │
                         │ Power BI / SID          │
                         │ APIs / future services  │
                         └─────────────────────────┘
```

---

## 7. Logical Components

### 7.1 Scheduler

The scheduler initiates media acquisition jobs.

Responsibilities:

- Execute jobs according to configured schedules.
- Identify feeds to process.
- Initiate acquisition workers.
- Track execution status.
- Prevent unintended duplicate runs.
- Record start/end times.
- Raise operational errors.

The existing SID design envisages scheduled media agents operating approximately 2–3 times per day, with the current-state description referring to approximately every two hours.

The final schedule should therefore be configuration rather than embedded application logic.

---

## 8. Media Acquisition Service

The Media Acquisition Service retrieves information from approved media sources.

### Responsibilities

1. Retrieve RSS feeds.
2. Validate the source against the approved source list.
3. Extract feed metadata.
4. Identify new articles.
5. Retrieve permitted article content where applicable.
6. Create an immutable raw record.
7. Publish a processing event.

### Source governance

Only approved sources should be processed.

The SID HLD requires external content used for sentiment analysis to originate from a curated, legally approved allow-list of domains and APIs.

Example source configuration:

```text
Source
 ├── source_id
 ├── source_name
 ├── feed_url
 ├── source_type
 ├── enabled
 ├── polling_frequency
 ├── legal_status
 └── configuration
```

---

## 9. Raw Media Store

Raw content is retained separately from processed intelligence.

The raw store contains immutable fetched articles/posts with date, source URL and text.

Example:

```text
RawArticle
-----------
id
source_id
source_url
title
published_at
retrieved_at
raw_content
content_hash
processing_status
created_at
```

The raw record provides the audit baseline from which subsequent processing can be reproduced or investigated.

---

## 10. Normalisation Service

Different sources will present content in different formats.

The Normalisation Service converts incoming content into a canonical article representation.

### Canonical model

```text
Article
-------
article_id
source_id
source_name
source_url
title
author
published_at
retrieved_at
content
language
content_hash
```

Normalisation may include:

- Removal of HTML.
- Removal of boilerplate.
- Whitespace normalisation.
- Encoding normalisation.
- Title extraction.
- Publication-date normalisation.
- Author extraction.
- Canonical URL creation.

---

## 11. Deduplication

The same story may appear:

- In multiple feeds.
- Under different URLs.
- As an updated article.
- Through syndicated content.
- With minor textual changes.

Deduplication should operate at multiple levels.

### Level 1 — URL

Exact URL comparison.

### Level 2 — Content hash

Exact or near-exact content comparison.

### Level 3 — Semantic similarity

AI/vector-based comparison may identify articles reporting substantially the same story.

The system should preserve duplicate relationships rather than simply deleting duplicate records.

Example:

```text
Article A
   │
   ├── canonical article
   │
   ├── duplicate Article B
   │
   └── duplicate Article C
```

This allows the number and distribution of sources reporting a story to remain available for future intelligence use.

---

## 12. AI-Assisted Filtering

The filtering stage determines whether an article is relevant enough to proceed to full intelligence processing.

A combination of deterministic and AI-based filtering is recommended.

### Rule-based filtering

Useful for high-confidence conditions:

- Source
- Keyword
- Organisation
- Topic
- Geography

### AI-assisted filtering

Useful where relevance depends on context.

For example, an article may contain "National Grid" but be unrelated to a topic being monitored.

The AI classifier should therefore determine contextual relevance rather than relying exclusively on keyword matching.

### Output

```text
relevance
relevance_score
relevance_reason
matched_topics
matched_entities
```

Low-relevance articles can be retained for audit purposes but need not enter the human review queue.

---

## 13. Classification and Tagging

Relevant articles are classified against a controlled taxonomy.

Example:

```text
Article
 |
 +-- Stakeholder
 |     +-- Organisation
 |     +-- Stakeholder type
 |
 +-- Sector
 |     +-- Electricity
 |     +-- Gas
 |     +-- Renewable energy
 |     +-- Networks
 |
 +-- Topic
 |     +-- Connections
 |     +-- Markets
 |     +-- Security
 |     +-- Regulation
 |     +-- Net Zero
 |
 +-- Geography
 |
 +-- Sentiment
 |
 +-- Relevance
```

The taxonomy should be managed as configuration/data rather than embedded in Python application code.

This allows business users to modify monitored topics without requiring a software release.

---

## 14. Entity Resolution

Entity extraction identifies organisations and other entities within the article.

Entity resolution maps different names to a canonical entity.

For example:

```text
"National Energy System Operator"
"NESO"
"the system operator"
```

may resolve to:

```text
entity_id = NESO
```

This is important because the SID reporting model needs media information related to named stakeholders and sectors.

---

## 15. Sentiment Analysis

The system may generate:

```text
sentiment_label
sentiment_score
confidence
sentiment_evidence
```

The sentiment should be associated with the article and, where possible, the relevant entity.

For example:

```text
Article
   |
   +-- NESO
   |     sentiment = neutral
   |
   +-- Energy Networks
         sentiment = positive
```

Sentiment is an analytical interpretation and must therefore remain traceable to the source content.

AI output must not be treated as independently verified fact.

---

## 16. AI Summarisation

The summarisation service generates a concise summary for human review.

The prompt should require the model to:

- Use only supplied article content.
- Avoid inventing facts.
- Preserve important names and dates.
- Distinguish reported facts from opinions.
- Avoid unsupported conclusions.
- Retain source attribution.
- Produce a consistent format.

Example:

```text
Summary
-------

Headline:
...

Key points:
1. ...
2. ...
3. ...

Relevant NESO stakeholder:
...

Relevant sector:
...

Potential significance:
...

Source:
...
```

The exact presentation format should be agreed during detailed design.

---

## 17. AI Processing Architecture

```text
                 ┌──────────────────────┐
                 │ Article              │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Relevance Agent      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Classification       │
                 │ / Tagging            │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Entity Resolution    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Sentiment Analysis   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Summarisation        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Review Queue         │
                 └──────────────────────┘
```

---

## 18. Processing Orchestration

The recommended processing pattern is an event-driven pipeline.

```text
MediaFetched
     │
     ▼
MediaNormalised
     │
     ▼
MediaDeduplicated
     │
     ▼
MediaFiltered
     │
     ▼
MediaClassified
     │
     ▼
MediaEnriched
     │
     ▼
MediaSummaryGenerated
     │
     ▼
ReviewRequired
     │
     ▼
Approved
     │
     ▼
Published
```

Each stage should be independently retryable.

A failed article should not prevent unrelated articles from continuing through the pipeline.

---

## 19. Messaging

An asynchronous messaging layer is recommended between processing stages.

Messages should contain identifiers and processing metadata rather than the complete article content.

Example:

```json
{
  "event_type": "media.article.normalised",
  "article_id": "123456",
  "correlation_id": "run-2026-09-26-001",
  "timestamp": "2026-09-26T18:00:00Z"
}
```

The consumer retrieves the article from the persistent store.

This provides:

- Loose coupling.
- Retry capability.
- Independent scaling.
- Failure isolation.
- Traceability.
- Future ability to add processing stages.

---

## 20. Processing Run

A processing run represents a scheduled execution.

```text
ProcessingRun
-------------
run_id
started_at
completed_at
status
articles_discovered
articles_processed
articles_rejected
articles_approved
articles_failed
```

This enables the operational UI to answer:

- When did the run start?
- How many articles were found?
- How many were relevant?
- How many were duplicates?
- How many required review?
- How many were approved?
- Were any processing failures encountered?

---

## 21. Review Workflow

The review service provides the human control point.

### Reviewer view

```text
--------------------------------------------------
Article
--------------------------------------------------
Source:        Example News
Published:     26 Sep 2026
URL:           ...

Title:
...

Original content
----------------
...

AI analysis
-----------
Relevance:     High
Classification:
   Electricity
   Connections

Entities:
   NESO
   ...

Sentiment:
   Neutral
   Confidence: 87%

Summary:
...

--------------------------------------------------
[ APPROVE ] [ REJECT ] [ NEEDS CHANGES ]
--------------------------------------------------
Reviewer rationale:
...
```

No AI-generated media intelligence should be published to the dashboard without review.

---

## 22. Review Data Model

```text
ReviewItem
----------
review_id
article_id
ai_result_id
status
reviewer_id
reviewed_at
decision
rationale
review_version
created_at
```

Possible statuses:

```text
PENDING
IN_REVIEW
APPROVED
REJECTED
CHANGES_REQUIRED
```

The review record should be immutable once the final decision has been made, subject to applicable audit and retention requirements.

---

## 23. Intelligence Store

The enriched data model should separate source information from AI-derived information.

### Article

```text
article_id
source_id
title
url
published_at
content
```

### Intelligence

```text
intelligence_id
article_id
relevance
classification
tags
entities
sentiment
sentiment_confidence
summary
ai_model
prompt_version
created_at
```

### Review

```text
review_id
intelligence_id
status
reviewer
decision
rationale
timestamp
```

This separation supports auditability and future reprocessing.

---

## 24. Database Architecture

The logical data layers are:

```text
Azure SQL
│
├── Raw
│   └── Raw articles
│
├── Normalised
│   └── Canonical articles
│
├── Intelligence
│   ├── classifications
│   ├── entities
│   ├── tags
│   ├── sentiment
│   └── summaries
│
└── Review
    ├── review items
    ├── decisions
    └── audit information
```

The exact physical schema belongs in the Detailed Design.

---

## 25. Integration with SID

The Media Intelligence Component should expose an API for approved intelligence.

```text
                  ┌─────────────────────┐
                  │ Media Intelligence  │
                  │ Component           │
                  └──────────┬──────────┘
                             │
                       Approved data
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Media Intelligence  │
                  │ API                 │
                  └──────────┬──────────┘
                             │ HTTPS
                             ▼
                  ┌─────────────────────┐
                  │ Strategic           │
                  │ Intelligence        │
                  │ Dashboard           │
                  └─────────────────────┘
```

The existing SID design defines the Media-to-Power BI interface as a REST API over HTTPS with OAuth2 authentication.

For the future architecture, Power BI should not become tightly coupled to internal MIC processing stores. The API or an approved analytics data layer should expose only the information required by SID.

---

## 26. API

Example high-level endpoints:

```text
GET /api/v1/media
GET /api/v1/media/{articleId}
GET /api/v1/intelligence
GET /api/v1/intelligence/{id}
GET /api/v1/topics
GET /api/v1/stakeholders
GET /api/v1/runs/{runId}
```

Operational endpoints:

```text
GET /health
GET /ready
GET /metrics
```

The exact API contract belongs in the Detailed Design.

---

## 27. Security

The component will follow NESO security principles.

### Security principles

- Microsoft Entra ID for human users.
- Application identities for service-to-service access.
- Least privilege.
- HTTPS/TLS for all external interfaces.
- No direct user access to persistence stores.
- Secrets stored in an approved secrets-management service.
- No credentials embedded in application code.
- Network access restricted to required endpoints.
- Approved media sources only.
- Audit logging of security-sensitive operations.

---

## 28. External Media Security

Media acquisition is an internet-facing capability and therefore requires additional controls.

The acquisition layer should:

- Use an allow-list.
- Restrict outbound destinations.
- Use HTTPS.
- Validate certificates.
- Enforce connection timeouts.
- Limit response sizes.
- Protect against malformed feeds.
- Record blocked sources.
- Record Zscaler/network blocks.
- Prevent arbitrary URL fetching based solely on article content.

---

## 29. Responsible AI

AI should support human judgement rather than replace it.

The architecture therefore implements:

```text
AI analysis
     │
     ▼
Human review
     │
 ┌───┴────┐
 │        │
Approve  Reject
 │
 ▼
Publish
```

AI output should retain:

- Source article.
- Source URL.
- Model.
- Processing timestamp.
- Classification.
- Confidence.
- Generated summary.
- Prompt/version where required.
- Reviewer decision.

This provides provenance and enables investigation of how an intelligence item was generated.

---

## 30. Data Quality

Data quality should be measured at each stage.

### Acquisition

- Feed available.
- Valid RSS.
- Article identifier.
- Source URL.
- Publication date.

### Normalisation

- Valid title.
- Usable article content.
- Canonical URL.
- Valid encoding.

### AI processing

- Relevance confidence.
- Classification confidence.
- Sentiment confidence.
- Summary generated.
- Source retained.

### Review

- Reviewer identified.
- Decision recorded.
- Rationale captured where required.

A data-quality status should be retained with the article rather than silently dropping problematic records.

---

## 31. Resilience and Error Handling

Individual article failures should not stop the pipeline.

```text
RSS unavailable
      │
      └── retry → dead-letter/error queue

Article unavailable
      │
      └── record acquisition failure

AI service unavailable
      │
      └── retry → queue

AI processing failure
      │
      └── retain article → retry

Review unavailable
      │
      └── retain item as PENDING
```

Every failure should contain:

```text
error_code
error_message
article_id
run_id
stage
timestamp
retry_count
```

---

## 32. Idempotency

Each processing stage must be idempotent.

If the same message is delivered twice, the second execution must not create an additional intelligence item.

A combination of:

```text
article_id
stage
processing_version
```

can be used as an idempotency key.

---

## 33. Observability

The system should provide end-to-end observability.

### Acquisition

- Feeds processed.
- Articles discovered.
- Articles failed.
- Feed response time.

### Processing

- Articles normalised.
- Duplicates.
- Relevant articles.
- Irrelevant articles.
- AI processing time.
- AI failures.

### Review

- Pending items.
- Approved.
- Rejected.
- Changes requested.
- Average review time.

### Publication

- Published items.
- API failures.
- Downstream failures.

---

## 34. Operational Dashboard

A lightweight operational UI should provide:

```text
Media Intelligence
────────────────────────────────────

Last successful run       18:04
Articles discovered      184
Duplicates                31
Relevant                  47
AI processed              47
Awaiting review            18
Approved                   24
Rejected                    5
Failed                      0

Feed status
────────────────────────────────────
Source A                  OK
Source B                  OK
Source C                  WARNING

Processing
────────────────────────────────────
Acquisition               OK
Normalisation             OK
Deduplication             OK
AI processing             OK
Review                    OK
Publication               OK
```

---

## 35. Performance and Scale

The current SID HLD estimates approximately **100–200 media items per month**, with approximately **10–20% approved for dashboard display**.

The architecture should nevertheless support substantially higher volumes because the component is intended to become a reusable NESO capability.

Scaling should be possible independently for:

- Acquisition.
- Normalisation.
- Deduplication.
- AI processing.
- Review.
- API access.

AI processing is likely to be the most computationally variable stage.

---

## 36. Availability

The SID requires 24×7 dashboard availability.

MIC should be designed so that temporary component failures do not result in loss of acquired media.

Persistence must occur before processing continues.

```text
Acquire
   ↓
Persist
   ↓
Process
```

rather than:

```text
Acquire
   ↓
Process
   ↓
Persist
```

This ensures that an AI or downstream service failure does not cause the source article to be lost.

---

## 37. Data Retention

Media content, processing records, review records and operational logs should be retained according to NESO retention policies.

Retention periods should be defined during Detailed Design with Security, Legal and Data Governance.

---

## 38. Deployment Architecture

A logical Azure deployment could be:

```text
Azure / NESO
│
├── Media Scheduler
├── Media Acquisition Service
├── Processing Workers
├── AI Services
├── Message Broker
├── Azure SQL
├── Review Application
├── Media Intelligence API
├── Application Insights
└── Log Analytics
```

The detailed choice between Azure Functions, Azure Container Apps or App Service should be made according to the operational and platform standards applicable to NESO.

---

## 39. Environment Strategy

The component should follow the SID environment model:

```text
Development
     ↓
System Test
     ↓
SIT
     ↓
Pre-Production
     ↓
Production
```

AI configuration should be version controlled across environments.

Production should not depend on developer-managed configuration.

---

## 40. Configuration

The following should be configurable without code changes:

- Media sources.
- RSS URLs.
- Source enable/disable status.
- Monitored stakeholders.
- Sectors.
- Topics.
- Keywords.
- Relevance thresholds.
- Classification taxonomy.
- AI model configuration.
- Processing schedule.
- Retry policies.
- Retention configuration.

---

## 41. Auditability

Every published intelligence item should be traceable:

```text
Published Intelligence
        │
        ▼
Review Decision
        │
        ▼
AI Output
        │
        ▼
Normalised Article
        │
        ▼
Raw Article
        │
        ▼
Original Source
```

This provides the provenance required for a governed intelligence capability.

---

## 42. Key Non-Functional Requirements

| Area | Requirement |
|---|---|
| Availability | Support continuous operation |
| Security | Entra ID/application identities and least privilege |
| Transport | HTTPS/TLS |
| Source governance | Approved media allow-list |
| Audit | End-to-end provenance |
| AI governance | Mandatory human review before publication |
| Scalability | Independent scaling of processing stages |
| Resilience | Retry and failure isolation |
| Idempotency | Safe reprocessing |
| Observability | End-to-end metrics, logs and tracing |
| Data retention | NESO retention policy |
| Maintainability | Configuration-driven taxonomy and sources |
| Traceability | Original source retained |
| Performance | Process normal media volumes without backlog |
| Extensibility | Support additional media sources and AI capabilities |

---

## 43. Key Design Principles

### 1. Source first

Every intelligence item must be traceable to its original source.

### 2. Persist before processing

Acquired content must be persisted before downstream AI processing.

### 3. Event-driven processing

Processing stages should be independently executable and retryable.

### 4. AI-assisted, not AI-authoritative

AI generates analysis; humans remain responsible for publication decisions.

### 5. Human in the loop

No AI-generated media intelligence is published to the dashboard without review.

### 6. Configuration over code

Sources, topics and taxonomy should be configurable.

### 7. Least privilege

Services receive only the permissions they require.

### 8. Observable by design

Every stage provides status, metrics, logs and correlation identifiers.

### 9. Independent scaling

High-volume processing stages can scale without scaling the entire system.

### 10. Reusable capability

MIC should be designed as a platform component that can support future NESO intelligence use cases.

---

## 44. Relationship to NESO Data & AI Strategy

The proposed component is aligned with NESO's stated direction for Data & AI.

NESO's direction includes bringing together data from multiple sources, improving data accessibility and interoperability, and using AI to generate insights that support evidence-based decision-making.

NESO's Digitalisation Strategy and Action Plan also describes a data platform, data quality programme, data-sharing infrastructure and an Advanced Analytics Environment supporting AI development and integration into NESO workflows.

MIC should therefore be regarded as an **intelligence-producing data capability**, rather than simply an RSS reader or media dashboard.

---

## 45. Future Evolution

The initial implementation should concentrate on media/RSS processing, but the architecture should allow additional sources.

Potential future sources include:

```text
RSS
 │
 ├── News APIs
 ├── Approved web sources
 ├── NESO publications
 ├── Industry publications
 ├── Regulatory publications
 └── Other approved information sources
```

Future AI capabilities could include:

- Topic trend detection.
- Emerging issue detection.
- Story clustering.
- Stakeholder relationship analysis.
- Cross-source comparison.
- Trend analysis over time.
- Event detection.
- Geographic analysis.
- Automated identification of significant changes.

These should be added without redesigning the core ingestion and review architecture.

---

## 46. High-Level End-to-End Flow

```text
                    ┌─────────────────┐
                    │ Approved RSS    │
                    │ Media Sources   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Scheduler       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Fetch Media     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Raw Store       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Normalise       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Deduplicate     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ AI Filtering    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Classify & Tag  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Entity          │
                    │ Resolution      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Sentiment       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Summarise       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Human Review    │
                    └───────┬─┬───────┘
                            │ │
                    Reject  │ │  Approve
                            │ │
                            │ └───────────┐
                            │             ▼
                            │    ┌─────────────────┐
                            │    │ Intelligence    │
                            │    │ Store           │
                            │    └────────┬────────┘
                            │             │
                            │             ▼
                            │    ┌─────────────────┐
                            │    │ MIC API         │
                            │    └────────┬────────┘
                            │             │
                            │             ▼
                            │    ┌─────────────────┐
                            │    │ SID / Power BI  │
                            │    └─────────────────┘
                            │
                            ▼
                       Audit Store
```

---

## 47. Architectural Decision Summary

| Decision | HLD Position |
|---|---|
| Media acquisition | RSS / approved external sources |
| Source governance | Allow-list |
| Processing model | Asynchronous pipeline |
| Persistence | Separate raw, normalised, enriched and review data |
| Deduplication | URL + content + semantic similarity |
| AI | Filtering, classification, tagging, entity extraction, sentiment and summarisation |
| Human review | Mandatory before publication |
| Integration | REST API for downstream consumers |
| Security | Entra ID/application identity, TLS, least privilege |
| Monitoring | Application telemetry + central logging |
| Deployment | Azure managed services |
| Primary reporting consumer | SID / Power BI |
| Future extensibility | Additional sources and intelligence capabilities |

---

## 48. Conclusion

The **Media Intelligence Component** provides NESO with a governed pipeline for converting external media into structured intelligence.

Its role is not simply to collect articles. It provides a controlled chain:

**Discover → Acquire → Persist → Normalise → Deduplicate → Filter → Classify → Tag → Analyse → Summarise → Review → Publish**

This directly supports the existing SID requirement for continuous media discovery, normalisation and enrichment, while maintaining the mandatory human review process before dashboard consumption.

The component also aligns with NESO's wider Data & AI direction: bringing together information from multiple sources, improving the ability to extract insights from data, and using AI to support evidence-based decision-making.

The component should therefore be treated as a **reusable NESO Media Intelligence capability**, with SID/Power BI being its initial consumer rather than its architectural boundary.

---

## Source Material

The HLD is based on:

1. **Strategic Intelligence Dashboard (SID) — High-Level Design**, supplied as part of this project.
2. **NESO — What We Do**
3. **NESO — Data & AI**
4. **NESO — Digitalisation Strategy and Action Plan**
