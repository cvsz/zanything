"""Queue and Worker Fabric abstractions, Job contracts, and lifecycle statuses."""

import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class JobStatus(StrEnum):
    """Lifecycle states for durable queued jobs."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    DEAD_LETTERED = "dead_lettered"


class JobPriority(StrEnum):
    """Execution priorities."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class Job(BaseModel):
    """Durable job payload and metadata."""

    id: str = Field(description="Unique Job UUID")
    tenant_id: str = Field(description="Tenant isolation boundary")
    task_name: str = Field(description="Registered worker handler name")
    payload: dict[str, Any] = Field(default_factory=dict, description="Job parameters")
    status: JobStatus = Field(
        default=JobStatus.PENDING, description="Current lifecycle state"
    )
    priority: JobPriority = Field(
        default=JobPriority.NORMAL, description="Scheduling priority"
    )
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    retry_count: int = Field(default=0, description="Current retry attempt")
    error_message: str | None = Field(default=None, description="Last failure reason")
    result: dict[str, Any] | None = Field(
        default=None, description="Job output on completion"
    )
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )


class WorkerHeartbeat(BaseModel):
    """Heartbeat signal and saturation status of an active worker instance."""

    worker_id: str
    hostname: str
    active_jobs: int
    max_concurrency: int
    saturation_pct: float
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
