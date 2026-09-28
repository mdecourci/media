# Media Intelligence Component — Pipeline Design

**Purpose:** Continuously discover media content about NESO's stakeholders and sectors, then filter, enrich and summarise it with AI so that only reviewed, governed insight reaches the Power BI dashboard.

**End-to-end flow:**

```
Discovery/Fetch → AI-Assisted Filtering → Classify & Tag → Summarise (AI agent)
   → Human Review (approve/reject/needs-changes) → Publish → Power BI
```

---

## 1. Discovery & Fetching

- Scheduler triggers time-based Worker jobs per configured stakeholder/sector keyword set.
- Workers pull from RSS feeds and other allow-listed, compliance-approved media sources/APIs, outbound-only over HTTPS/TLS 1.2+.
- Fetched items (source URL, publish date, full text) are written immutably to the **Raw Store** — nothing is discarded at this stage, so every fetch is auditable even if later filtered out.

## 2. AI-Assisted Filtering

- **Allow-list check** at content level (needed because some feeds aggregate multiple origins).
- **Relevance filter** — does the item genuinely relate to a tracked stakeholder or sector? Threshold is configurable so review volume can be tuned without a code change.
- **Deduplication** — collapses syndicated/near-duplicate stories covering the same event.
- Everything discarded here is logged with a reason (not allow-listed / not relevant / duplicate) for audit and threshold tuning.
- Surviving items move to the **Normalised Store**: clean text, canonical title/body fields.

## 3. Classify & Tag

- **Entity resolution** against the stakeholder/segment taxonomy already used in Salesforce (e.g., Scottish Power Networks, SSE Networks; Sea Communities, Visual Impact Groups).
- **Sentiment scoring** with a confidence value.
- **Multi-label tagging** where one item spans more than one stakeholder/segment.
- Low-confidence classifications are flagged distinctly so reviewers give them closer attention rather than the item auto-passing.
- Output persisted to the **Enriched Store** (entities, sentiment, confidence), traceable back to the Raw and Normalised records.

## 4. Summarise (AI Agent)

- The AI agent generates a concise, dashboard-length summary of each enriched item — key facts, named entities, overall sentiment.
- The summary, the source article, and its classification/sentiment output are packaged together as one reviewable record — a reviewer never has to hunt across stores to make a decision.

## 5. Human-in-the-Loop Review

- Lightweight review UI: work queue (new/flagged), side-by-side "source vs AI output," confidence scores.
- Reviewer actions: **Approve / Reject / Needs-changes**, with rationale and tags captured.
- Decision, reviewer identity, timestamp and rationale are written to the **Review Store** — this is also the feedback signal used to improve future filtering, classification and summarisation quality.

## 6. Publish

- The **Publish Orchestrator** promotes only *approved* items from the Review Store to the analytics storage layer Power BI reads from.
- Rejected/needs-changes items never reach the dashboard.

---

## Operational Notes (carried from the existing design)

- Cadence: agents run ~2–3 times/day, 6am–6pm.
- Zscaler-blocked sources are logged as part of error handling.
- Run status, freshness and error queues are visible via an Operational UI for Ops/Support.
