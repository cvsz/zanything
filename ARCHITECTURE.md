# Actions / OpenAPI Architecture

Use Actions when the GPT needs to interact with APIs you control.

## Recommended service pattern

GPT
→ Action API Gateway
→ AuthN/AuthZ
→ Policy / confirmation layer
→ Task service
→ Worker / provider adapter
→ Audit log
→ Result store

## Requirements

- TLS only
- Strong authentication
- Scoped authorization
- Tenant isolation when multi-tenant
- Request validation
- Rate limiting
- Idempotency for writes
- Audit logging
- Safe retries
- Explicit destructive-operation policy
- Secret isolation
- Timeouts
- Clear error responses
- No hidden side effects

## Action classes

### Read-only
Examples:
- fetch status
- search internal catalog
- query metrics

### Reversible write
Examples:
- create draft
- create task
- create branch

### High impact
Examples:
- deploy production
- merge PR
- delete data
- send public message
- rotate credentials

High-impact actions must obey platform/user confirmation requirements.

## Suggested endpoints

- POST /tasks
- GET /tasks/{id}
- POST /drafts
- GET /status
- POST /validate
- POST /artifacts
