# Research / Deep Research Implementation Prompt

Implement production Research and Deep Research capabilities for zanything.

## Required system properties
- Explicit research question and sub-question planning.
- Freshness-aware retrieval strategy.
- Primary-source preference where available.
- Secondary-source contextualization.
- Source deduplication.
- Contradiction detection and unresolved-claim tracking.
- Evidence/provenance graph.
- Citation integrity validation.
- Clear separation of fact, inference, estimate, and recommendation.
- Confidence/uncertainty signaling without fabricated precision.
- Deep-research report rendering.
- Tenant-safe persistence of research artifacts.

## Implementation requirements
- Define data models for research plan, source, claim, evidence edge, citation, contradiction, and report.
- Make retrieval/provider interfaces replaceable.
- Store source timestamps and provenance metadata.
- Add deterministic validation for missing/invalid citations.
- Support resumable research jobs.
- Add observability for retrieval latency, source failures, duplicate rate, citation failures, and job completion.
- Add retention and deletion hooks.

## Test requirements
- source dedupe
- stale-source detection
- primary-source preference
- contradictory-source handling
- citation-to-claim linkage
- missing citation rejection
- resumability
- tenant isolation
- provider outage/degraded mode
- no fabricated source success

## Definition of done
Do not mark complete until the research engine, tests, docs, evals, operational metrics, and release evidence exist.
