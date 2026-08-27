# Operations Runbook: Identity Access Review & Break-Glass Procedures

## 1. Overview
This runbook defines operational protocols for identity verification, quarterly user access reviews, and emergency break-glass procedure for `zanything`.

---

## 2. Access Review Protocol (Quarterly)
1. **Audit Extraction**:
   - Query `/v1/admin/roles` to inspect the active role definitions and permission mappings.
   - Extract service account registry from configuration and verify all assigned keys against active owners.
2. **Review Checklist**:
   - Verify least-privilege principle: remove any unneeded `Role.ADMIN` assignments.
   - Decommission inactive service accounts and revoke expired API keys.
   - Validate tenant boundaries: ensure service account scopes are constrained to their respective `tenant_id`.

---

## 3. Emergency Break-Glass Procedure
In the event of an identity provider (OIDC/IdP) outage or lockout:

1. **Activate Break-Glass Credentials**:
   - Provision a temporary, high-entropy service account API key directly via encrypted environment secret (`ZANYTHING_SERVICE_ACCOUNT_API_KEYS`).
2. **Session Audit**:
   - All break-glass operations will be tagged in structured logs with `subject: "break-glass-admin"` and unique `request_id`.
3. **Revocation & Post-Mortem**:
   - Immediately rotate or remove break-glass credentials once IdP availability is restored.
   - Export audit logs using the correlation ID and archive within 24 hours.
