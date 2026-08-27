"""Request and response models."""

from typing import Any

from pydantic import BaseModel, Field


class ExecuteRequest(BaseModel):
    """Incoming execution request."""

    objective: str = Field(min_length=1, max_length=20000)
    context: dict[str, Any] = Field(default_factory=dict)
    requested_modes: list[str] = Field(default_factory=list)
    dry_run: bool = False
    require_verification: bool = True


class ExecuteResponse(BaseModel):
    """Execution response — currently returns routing result only."""

    request_id: str
    status: str
    objective: str
    modes: list[str]
    workflow: list[str]
    dry_run: bool
    verification_required: bool
