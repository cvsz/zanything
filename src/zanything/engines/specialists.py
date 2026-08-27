"""Specialist domain execution engines (Data, Project OS, Multimodal)."""

import datetime
from typing import Any

from pydantic import BaseModel, Field

from zanything.logging import get_logger

logger = get_logger("zanything.engines.specialists")


class DataProfileReport(BaseModel):
    """Profiling metrics for ingested datasets."""

    dataset_name: str
    total_rows: int
    column_types: dict[str, str]
    missing_values: dict[str, int]
    anomalies_detected: list[str] = Field(default_factory=list)


class DataEngine:
    """Ingests, profiles, and detects anomalies in tabular datasets."""

    def profile_records(
        self, dataset_name: str, records: list[dict[str, Any]]
    ) -> DataProfileReport:
        total_rows = len(records)
        if not records:
            return DataProfileReport(
                dataset_name=dataset_name,
                total_rows=0,
                column_types={},
                missing_values={},
            )

        col_types: dict[str, str] = {}
        missing: dict[str, int] = {}
        anomalies: list[str] = []

        keys = records[0].keys()
        for k in keys:
            missing[k] = sum(1 for r in records if r.get(k) is None or r.get(k) == "")
            types = {type(r.get(k)).__name__ for r in records if r.get(k) is not None}
            col_types[k] = "/".join(types) if types else "null"
            if len(types) > 1:
                anomalies.append(f"Column '{k}' has mixed data types: {col_types[k]}")

        return DataProfileReport(
            dataset_name=dataset_name,
            total_rows=total_rows,
            column_types=col_types,
            missing_values=missing,
            anomalies_detected=anomalies,
        )


class ProjectMilestone(BaseModel):
    """Project milestone entity in Project OS."""

    milestone_id: str
    title: str
    completed: bool = False
    dependencies: list[str] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)


class ProjectOS:
    """Project state machine, dependency DAG tracker, and completion ledger."""

    def __init__(self, project_id: str, tenant_id: str) -> None:
        self.project_id = project_id
        self.tenant_id = tenant_id
        self.milestones: dict[str, ProjectMilestone] = {}

    def add_milestone(self, milestone: ProjectMilestone) -> None:
        self.milestones[milestone.milestone_id] = milestone

    def mark_complete(self, milestone_id: str) -> bool:
        ms = self.milestones.get(milestone_id)
        if not ms:
            return False
        # Check dependencies
        for dep_id in ms.dependencies:
            dep = self.milestones.get(dep_id)
            if not dep or not dep.completed:
                logger.warning(
                    f"Cannot complete '{milestone_id}': "
                    f"dependency '{dep_id}' is pending."
                )
                return False
        ms.completed = True
        logger.info(f"Project '{self.project_id}' completed milestone: {milestone_id}")
        return True

    def get_progress_pct(self) -> float:
        if not self.milestones:
            return 0.0
        completed = sum(1 for m in self.milestones.values() if m.completed)
        return round((completed / len(self.milestones)) * 100, 2)


class MultimodalInputModel(BaseModel):
    """Unified file, image, data, and prompt input payload."""

    tenant_id: str
    prompt: str
    image_refs: list[str] = Field(default_factory=list)
    data_refs: list[str] = Field(default_factory=list)
    context_tokens: int = 0
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
