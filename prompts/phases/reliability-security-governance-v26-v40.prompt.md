# Phase Prompt — v26–v40 Reliability, Security & Governance

Implement cross-cutting production reliability, security and governance after the universal capability runtime is integrated.

## Scope
- v26 Memory & Context Governance
- v27 Observability Productionization
- v28 SLO/SLA Layer
- v29 Resilience Engineering
- v30 Backup/Restore/DR
- v31 Security Hardening
- v32 Supply Chain Security
- v33 CI/CD Production Pipeline
- v34 Environment Strategy
- v35 Release Management
- v36 Performance Engineering
- v37 Cost Governance
- v38 Compliance Foundation
- v39 Privacy & Data Governance
- v40 Audit & Forensics

## Requirements
- Cross-tenant leakage tests and retention/reset controls.
- OpenTelemetry-compatible traces, structured logs, RED metrics and actionable alerts.
- Defined SLOs, error budgets and burn-rate alerts.
- Circuit breakers, bulkheads, backpressure, timeout budgets and chaos tests.
- Encrypted backups, tested restore, PITR strategy and RPO/RTO.
- Web/API hardening and abuse controls.
- SAST/SCA/DAST/container/IaC/secret scanning gates.
- SBOM, provenance and signed release artifacts where supported.
- Dev/test/staging/preprod/prod separation.
- SemVer, migration compatibility and immutable release process.
- Load/soak/capacity evidence.
- Cost/quotas/tenant limits.
- Privacy, PII, retention, deletion/export and evidence controls.
- Append-only/tamper-evident audit strategy and investigation workflows.

## Exit gate
No production-readiness claim is allowed until all applicable security, resilience, backup/restore, observability, privacy and audit controls are operational and evidenced.
