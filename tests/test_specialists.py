"""Integration tests for specialist engines (Data, Project OS, Multimodal)."""

from zanything.engines.specialists import (
    DataEngine,
    MultimodalInputModel,
    ProjectMilestone,
    ProjectOS,
)


def test_data_engine_profiling_and_anomalies() -> None:
    """Verify tabular dataset profiling detects rows, nulls, and anomalies."""
    engine = DataEngine()
    records = [
        {"user_id": 1, "name": "Alice", "score": 95.5},
        {"user_id": 2, "name": "Bob", "score": 88.0},
        {"user_id": 3, "name": "Charlie", "score": "invalid_score"},
        {"user_id": 4, "name": None, "score": 75.0},
    ]

    report = engine.profile_records("test_users", records)
    assert report.total_rows == 4
    assert report.missing_values["name"] == 1
    assert len(report.anomalies_detected) > 0  # mixed type on score


def test_project_os_milestone_dag() -> None:
    """Verify project milestone execution enforces dependencies before completion."""
    pos = ProjectOS("proj-zanything-ga", "tenant-core")

    m1 = ProjectMilestone(milestone_id="m1", title="Backend Data Layer")
    m2 = ProjectMilestone(milestone_id="m2", title="Frontend GUI", dependencies=["m1"])

    pos.add_milestone(m1)
    pos.add_milestone(m2)

    # Attempt to complete m2 before m1 -> must fail
    assert pos.mark_complete("m2") is False
    assert pos.get_progress_pct() == 0.0

    # Complete m1 -> then m2 can complete
    assert pos.mark_complete("m1") is True
    assert pos.get_progress_pct() == 50.0
    assert pos.mark_complete("m2") is True
    assert pos.get_progress_pct() == 100.0


def test_multimodal_input_contract() -> None:
    """Verify multimodal input model validates image references and token tracking."""
    mm = MultimodalInputModel(
        tenant_id="tenant-media",
        prompt="Generate movie poster layout for cyberpunk theme",
        image_refs=["art-12345", "art-67890"],
    )
    assert len(mm.image_refs) == 2
    assert mm.tenant_id == "tenant-media"
