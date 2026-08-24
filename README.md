## Stage 1 — Minimal database persistence

Goal: prove the smallest possible ingestion path.

Build:
Payload → SQL

Python
  ↓
hard-coded MediaEnvelope
  ↓
SQLAlchemy
  ↓
PostgreSQL

### Implement:

* Content model
* IngestionMetadata model
* async SQLAlchemy
* database transaction
* basic configuration
* unit tests
* integration test