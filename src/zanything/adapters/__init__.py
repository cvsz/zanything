"""Universal Integration Fabric adapter contracts and reference adapters."""

from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from zanything.logging import get_logger

logger = get_logger("zanything.adapters")


class AdapterCategory(StrEnum):
    """Supported external integration categories."""

    CODE_VCS = "code_vcs"  # GitHub, GitLab
    COMMUNICATION = "communication"  # Slack, Teams
    WORKSPACE = "workspace"  # Google Workspace, Microsoft 365
    PROJECT_MANAGEMENT = "project_management"  # Jira, Linear, Notion
    STORAGE_DATA = "storage_data"  # S3, Postgres, Custom API


class IntegrationContext(BaseModel):
    """Context passed to integration adapter operations."""

    tenant_id: str
    actor_id: str
    request_id: str
    scopes: list[str] = Field(default_factory=list)


class IntegrationResult(BaseModel):
    """Result of an integration operation."""

    success: bool
    data: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None
    audit_metadata: dict[str, Any] = Field(default_factory=dict)


class BaseIntegrationAdapter(ABC):
    """Universal contract for third-party integration adapters."""

    def __init__(self, adapter_id: str, category: AdapterCategory) -> None:
        self.adapter_id = adapter_id
        self.category = category

    @abstractmethod
    async def check_health(self) -> bool:
        """Check if integration endpoint is reachable and credentials are valid."""
        pass

    @abstractmethod
    async def execute(
        self, action: str, params: dict[str, Any], context: IntegrationContext
    ) -> IntegrationResult:
        """Execute action through integration adapter."""
        pass


class GitHubAdapter(BaseIntegrationAdapter):
    """GitHub integration adapter for repository, issues, and PR management."""

    def __init__(self, api_token: str | None = None) -> None:
        super().__init__(adapter_id="github", category=AdapterCategory.CODE_VCS)
        self.api_token = api_token

    async def check_health(self) -> bool:
        return True

    async def execute(
        self, action: str, params: dict[str, Any], context: IntegrationContext
    ) -> IntegrationResult:
        logger.info(
            f"GitHub adapter executing '{action}' for tenant '{context.tenant_id}'"
        )
        if action == "create_issue":
            return IntegrationResult(
                success=True,
                data={
                    "issue_id": 101,
                    "title": params.get("title", ""),
                    "url": "https://github.com/org/repo/issues/101",
                },
                audit_metadata={"action": "create_issue", "repo": params.get("repo")},
            )
        return IntegrationResult(
            success=False, error_message=f"Unsupported action: {action}"
        )


class SlackAdapter(BaseIntegrationAdapter):
    """Slack integration adapter for notifications and interactive messaging."""

    def __init__(self, webhook_url: str | None = None) -> None:
        super().__init__(adapter_id="slack", category=AdapterCategory.COMMUNICATION)
        self.webhook_url = webhook_url

    async def check_health(self) -> bool:
        return True

    async def execute(
        self, action: str, params: dict[str, Any], context: IntegrationContext
    ) -> IntegrationResult:
        logger.info(
            f"Slack adapter sending message to '{params.get('channel')}' "
            f"for tenant '{context.tenant_id}'"
        )
        return IntegrationResult(
            success=True,
            data={"channel": params.get("channel"), "delivered": True},
            audit_metadata={"channel": params.get("channel")},
        )
