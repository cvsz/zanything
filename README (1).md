# Automated Integration Framework

Implement each external service as an adapter inheriting from `base.py`.

Recommended categories:

- AI/model providers
- search/retrieval
- GitHub/GitLab
- Google Workspace / Microsoft 365
- Slack / Teams / email
- databases
- Redis/queues
- object storage
- Jira / Linear
- observability
- internal HTTP APIs

Mandatory rules:

- least-privilege credentials
- scoped permissions
- bounded timeouts
- safe retries
- idempotency for writes
- secret redaction
- normalized errors
- audit/request ID propagation
- health reporting
- confirmation gating for high-impact actions
