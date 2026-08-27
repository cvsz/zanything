"""Identity and Access Management (IAM) contracts and principal models."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SubjectType(StrEnum):
    """Subject type of the authenticated principal."""

    USER = "user"
    SERVICE_ACCOUNT = "service_account"
    API_KEY = "api_key"


class Role(StrEnum):
    """Predefined enterprise RBAC roles."""

    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"
    AUDITOR = "auditor"


class Principal(BaseModel):
    """Authenticated identity principal with tenant and role context."""

    subject: str = Field(
        description="Unique identifier for the user or service account"
    )
    subject_type: SubjectType = Field(
        default=SubjectType.USER, description="Type of subject"
    )
    tenant_id: str = Field(default="default", description="Tenant isolation identifier")
    roles: list[Role | str] = Field(
        default_factory=list, description="Assigned RBAC roles"
    )
    scopes: list[str] = Field(
        default_factory=list, description="OAuth/OIDC granted scopes"
    )
    email: str | None = Field(
        default=None, description="User email address if available"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional claims and attributes for ABAC"
    )

    def has_role(self, role: Role | str) -> bool:
        """Check if principal has a specific role or is an admin."""
        return Role.ADMIN in self.roles or "admin" in self.roles or role in self.roles

    def has_scope(self, scope: str) -> bool:
        """Check if principal has the requested OAuth scope."""
        return scope in self.scopes or "*" in self.scopes or "admin" in self.scopes
