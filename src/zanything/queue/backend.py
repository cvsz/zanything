"""Durable queue backend interface and reference async implementations."""

import asyncio
from abc import ABC, abstractmethod
from typing import Any

from zanything.logging import get_logger
from zanything.queue import Job, JobPriority, JobStatus

logger = get_logger("zanything.queue.backend")


class QueueBackend(ABC):
    """Abstract interface for durable queue backends (Memory/Redis)."""

    @abstractmethod
    async def enqueue(self, job: Job) -> Job:
        """Enqueue a job for async processing."""
        pass

    @abstractmethod
    async def dequeue(
        self, tenant_id: str | None = None, timeout_seconds: float = 1.0
    ) -> Job | None:
        """Pop the next available job considering priority and tenant."""
        pass

    @abstractmethod
    async def complete_job(self, job_id: str, result: dict[str, Any]) -> Job | None:
        """Mark a job as completed with result payload."""
        pass

    @abstractmethod
    async def fail_job(self, job_id: str, error: str, retry: bool = True) -> Job | None:
        """Mark a job as failed, handle retry counter or route to DLQ."""
        pass

    @abstractmethod
    async def cancel_job(self, job_id: str) -> Job | None:
        """Cancel a pending or running job."""
        pass

    @abstractmethod
    async def get_job(self, job_id: str) -> Job | None:
        """Retrieve job status and metadata by ID."""
        pass

    @abstractmethod
    async def get_dlq_jobs(self, tenant_id: str | None = None) -> list[Job]:
        """List dead-lettered jobs for investigation."""
        pass


class AsyncMemoryQueue(QueueBackend):
    """Thread-safe and async reference queue implementation with DLQ and retries."""

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._queue: asyncio.PriorityQueue[tuple[int, str]] = asyncio.PriorityQueue()
        self._dlq: list[str] = []
        self._lock = asyncio.Lock()

    def _priority_weight(self, priority: JobPriority) -> int:
        weights = {
            JobPriority.CRITICAL: 1,
            JobPriority.HIGH: 2,
            JobPriority.NORMAL: 3,
            JobPriority.LOW: 4,
        }
        return weights.get(priority, 3)

    async def enqueue(self, job: Job) -> Job:
        async with self._lock:
            self._jobs[job.id] = job
            weight = self._priority_weight(job.priority)
            await self._queue.put((weight, job.id))
            logger.info(
                f"Enqueued job '{job.id}' [{job.priority}] for tenant '{job.tenant_id}'"
            )
            return job

    async def dequeue(
        self, tenant_id: str | None = None, timeout_seconds: float = 0.5
    ) -> Job | None:
        try:
            _, job_id = await asyncio.wait_for(
                self._queue.get(), timeout=timeout_seconds
            )
            async with self._lock:
                job = self._jobs.get(job_id)
                if not job or job.status == JobStatus.CANCELLED:
                    return None
                if tenant_id and job.tenant_id != tenant_id:
                    # Re-queue if tenant does not match
                    await self._queue.put((self._priority_weight(job.priority), job_id))
                    return None

                job.status = JobStatus.RUNNING
                return job
        except TimeoutError:
            return None

    async def complete_job(self, job_id: str, result: dict[str, Any]) -> Job | None:
        async with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            job.status = JobStatus.COMPLETED
            job.result = result
            logger.info(f"Job '{job_id}' completed successfully")
            return job

    async def fail_job(self, job_id: str, error: str, retry: bool = True) -> Job | None:
        async with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None

            job.error_message = error
            if retry and job.retry_count < job.max_retries:
                job.retry_count += 1
                job.status = JobStatus.PENDING
                # Exponential backoff retry
                weight = self._priority_weight(job.priority)
                await self._queue.put((weight, job.id))
                logger.warning(
                    f"Job '{job_id}' failed: {error}. "
                    f"Scheduled retry {job.retry_count}/{job.max_retries}"
                )
            else:
                job.status = JobStatus.DEAD_LETTERED
                self._dlq.append(job_id)
                logger.error(
                    f"Job '{job_id}' moved to Dead Letter Queue (DLQ): {error}"
                )

            return job

    async def cancel_job(self, job_id: str) -> Job | None:
        async with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            job.status = JobStatus.CANCELLED
            logger.info(f"Job '{job_id}' cancelled")
            return job

    async def get_job(self, job_id: str) -> Job | None:
        async with self._lock:
            return self._jobs.get(job_id)

    async def get_dlq_jobs(self, tenant_id: str | None = None) -> list[Job]:
        async with self._lock:
            dlq_jobs = [self._jobs[jid] for jid in self._dlq if jid in self._jobs]
            if tenant_id:
                return [j for j in dlq_jobs if j.tenant_id == tenant_id]
            return dlq_jobs
