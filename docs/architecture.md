# Architecture

## Current State (v0.1.0)

zanything is a FastAPI application that performs keyword-based intent routing across 20+ specialist modes.

### Components

```
┌─────────────────────────────────────────────┐
│  Client (GUI / API consumer)                │
│  index.html or HTTP client                  │
└──────────────┬──────────────────────────────┘
               │ HTTP
┌──────────────▼──────────────────────────────┐
│  FastAPI Application (zanything.app)        │
│                                              │
│  ┌────────────┐  ┌───────────────────────┐  │
│  │  Routing   │  │  Models               │  │
│  │  (keyword) │  │  (Pydantic req/resp)  │  │
│  └────────────┘  └───────────────────────┘  │
│                                              │
│  Endpoints:                                  │
│  GET  /healthz, /readyz, /version           │
│  GET  /v1/capabilities                      │
│  POST /v1/execute                           │
└──────────────────────────────────────────────┘
```

### What exists

- Keyword-based mode routing (20 modes)
- Workflow step generation
- Request ID propagation
- Dry-run support
- Basic GUI console

### What does NOT exist yet

- Authentication / authorization (v5)
- Database / persistence (v6)
- Queue / worker system (v7)
- Provider execution (v8)
- Integration adapters (v9)
- Secret management (v10)

### Design Principles

- TLS only in production
- Strong authentication (planned: OIDC/JWT)
- Scoped authorization (planned: RBAC + ABAC)
- Tenant isolation when multi-tenant
- Request validation via Pydantic
- Idempotency for writes (header accepted, not enforced yet)
- Audit logging (planned)
- Explicit destructive-operation policy (planned)
- No hidden side effects

### Action Classes (planned)

| Class | Examples | Policy |
|---|---|---|
| Read-only | fetch status, search, query metrics | No confirmation needed |
| Reversible write | create draft, create task, create branch | Standard confirmation |
| High impact | deploy production, merge PR, delete data | Requires explicit approval |

See [`roadmap/exec-planning.md`](../roadmap/exec-planning.md) for the full implementation plan.
