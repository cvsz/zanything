"""Request and response models."""

from typing import Any

from pydantic import BaseModel, Field


class ExecuteRequest(BaseModel):
    """Incoming execution request."""

    objective: str = Field(
        min_length=1, max_length=20000, description="The user goal or task"
    )
    context: dict[str, Any] = Field(
        default_factory=dict, description="Execution context & state"
    )
    requested_modes: list[str] = Field(
        default_factory=list, description="Explicit mode override"
    )
    dry_run: bool = Field(
        default=False, description="Simulate routing without execution"
    )
    require_verification: bool = Field(
        default=True, description="Enforce verification step"
    )


class ExecuteResponse(BaseModel):
    """Execution response — currently returns routing plan."""

    request_id: str = Field(description="Unique correlation ID for this request")
    status: str = Field(description="Execution lifecycle status")
    objective: str = Field(description="Normalized objective")
    modes: list[str] = Field(description="Selected execution modes")
    workflow: list[str] = Field(description="Workflow pipeline sequence")
    dry_run: bool = Field(description="Whether dry-run mode was requested")
    verification_required: bool = Field(description="Whether verification is enforced")


class HealthResponse(BaseModel):
    """Service liveness and readiness response."""

    status: str = Field(description="Health status indicator")
    app: str = Field(description="Application identifier")
    version: str = Field(description="Application version")
    uptime_seconds: float | None = Field(
        default=None, description="Service uptime in seconds"
    )
    dependencies: dict[str, str] = Field(
        default_factory=dict, description="Status of required external dependencies"
    )


class CapabilityResponse(BaseModel):
    """Capabilities and supported modes response."""

    modes: list[str] = Field(description="Available capability modes")
    features: list[str] = Field(
        description="Platform features active in current runtime"
    )
