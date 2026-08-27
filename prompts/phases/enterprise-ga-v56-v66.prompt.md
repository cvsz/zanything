# Phase Prompt — v56–v66 Enterprise GA & Gold Master

Complete zanything for Enterprise GA only after all earlier platform, capability, security, reliability and distribution gates are evidenced.

## Scope
- v56 Documentation Complete
- v57 Operations Handbook
- v58 Supportability
- v59 Enterprise Branding / White-label
- v60 Entitlement Layer
- v61 Offline / Air-Gapped Profile
- v62 Production Security Review
- v63 Production Readiness Review
- v64 Gold Master Release Gate
- v65 Enterprise GA
- v66 Post-GA Continuous Operations

## Required deliverables
- Complete architecture, API, deployment, security, admin, operator, user, integration, SDK and troubleshooting documentation.
- On-call, severity, escalation, incident, maintenance, release, key-rotation, capacity and restore procedures.
- Diagnostic/self-check bundle with secret redaction.
- Safe branding/customization boundaries.
- Entitlements and quotas kept separate from authorization semantics.
- Offline install/update/provider profile when supported.
- Full production security review with formal treatment for any remaining Critical/High findings.
- Production Readiness Review covering capacity, SLOs, backup/restore, DR, security, observability, ownership, upgrade and rollback.
- Gold Master evidence: clean install, all required tests/scans, restore, migration, upgrade and rollback proof, release documentation and archived evidence.
- Immutable GA release with release notes, SBOM, provenance, deployment manifest and compatibility matrix.
- Post-GA vulnerability/patch SLA, dependency maintenance, periodic restore/access/capacity reviews, eval regression and incident-learning loop.

## Hard release rule
Do not call the system `Production-Grade Ready`, `Enterprise-Grade Ready`, `Gold Master`, or `GA` based on plans or partial evidence. The designation is permitted only after `GOLD-MASTER-CHECKLIST.md` and v64/v65 are satisfied with recorded evidence.
