"""Tests for v7 Queue & Worker Fabric (Retries, Priority, Heartbeats, DLQ)."""

from typing import Any

import pytest

from zanything.queue import Job, JobPriority, JobStatus
from zanything.queue.backend import AsyncMemoryQueue
from zanything.queue.worker import Worker


@pytest.mark.anyio
async def test_job_enqueue_dequeue_completion() -> None:
    """Enqueue a job and process it successfully through Worker."""
    queue = AsyncMemoryQueue()
    worker = Worker(worker_id="worker-01", queue_backend=queue)

    async def mock_handler(payload: dict[str, Any]) -> dict[str, Any]:
        return {"processed": True, "input_len": len(payload.get("data", ""))}

    worker.register_handler("process_data", mock_handler)

    job = Job(
        id="job-100",
        tenant_id="tenant-queue-test",
        task_name="process_data",
        payload={"data": "hello queue"},
    )
    await queue.enqueue(job)

    # Process job
    executed = await worker.execute_one()
    assert executed is True

    # Check completed state
    completed_job = await queue.get_job("job-100")
    assert completed_job is not None
    assert completed_job.status == JobStatus.COMPLETED
    assert completed_job.result == {"processed": True, "input_len": 11}


@pytest.mark.anyio
async def test_priority_scheduling() -> None:
    """Verify CRITICAL priority jobs are popped before NORMAL priority jobs."""
    queue = AsyncMemoryQueue()

    normal_job = Job(
        id="job-normal",
        tenant_id="tenant-test",
        task_name="dummy",
        priority=JobPriority.NORMAL,
    )
    critical_job = Job(
        id="job-critical",
        tenant_id="tenant-test",
        task_name="dummy",
        priority=JobPriority.CRITICAL,
    )

    await queue.enqueue(normal_job)
    await queue.enqueue(critical_job)

    first_popped = await queue.dequeue()
    assert first_popped is not None
    assert first_popped.id == "job-critical"


@pytest.mark.anyio
async def test_retry_and_dead_letter_queue() -> None:
    """Verify job failure triggers retries and eventually routes to DLQ."""
    queue = AsyncMemoryQueue()
    worker = Worker(worker_id="worker-fail-test", queue_backend=queue)

    async def failing_handler(_payload: dict[str, Any]) -> dict[str, Any]:
        raise RuntimeError("Simulated external service timeout")

    worker.register_handler("failing_task", failing_handler)

    job = Job(
        id="job-dlq-test",
        tenant_id="tenant-dlq",
        task_name="failing_task",
        max_retries=2,
    )
    await queue.enqueue(job)

    # Attempt 1 -> Retry 1
    await worker.execute_one()
    j1 = await queue.get_job("job-dlq-test")
    assert j1 is not None
    assert j1.retry_count == 1
    assert j1.status == JobStatus.PENDING

    # Attempt 2 -> Retry 2
    await worker.execute_one()
    j2 = await queue.get_job("job-dlq-test")
    assert j2 is not None
    assert j2.retry_count == 2

    # Attempt 3 -> DLQ
    await worker.execute_one()
    j3 = await queue.get_job("job-dlq-test")
    assert j3 is not None
    assert j3.status == JobStatus.DEAD_LETTERED

    dlq_jobs = await queue.get_dlq_jobs(tenant_id="tenant-dlq")
    assert len(dlq_jobs) == 1
    assert dlq_jobs[0].id == "job-dlq-test"


@pytest.mark.anyio
async def test_worker_heartbeat_and_saturation() -> None:
    """Verify worker heartbeat reporting and saturation metrics."""
    queue = AsyncMemoryQueue()
    worker = Worker(worker_id="worker-node-1", queue_backend=queue, max_concurrency=4)
    worker.active_jobs = 2

    hb = worker.get_heartbeat()
    assert hb.worker_id == "worker-node-1"
    assert hb.active_jobs == 2
    assert hb.max_concurrency == 4
    assert hb.saturation_pct == 50.0
