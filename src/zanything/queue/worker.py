"""Worker fabric executor with concurrency controls and heartbeats."""

import asyncio
import socket
from collections.abc import Awaitable, Callable
from typing import Any

from zanything.logging import get_logger, request_id_ctx, tenant_id_ctx
from zanything.queue import Job, WorkerHeartbeat
from zanything.queue.backend import QueueBackend

logger = get_logger("zanything.queue.worker")

TaskHandler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


class Worker:
    """Async worker pool executing registered task handlers."""

    def __init__(
        self,
        worker_id: str,
        queue_backend: QueueBackend,
        max_concurrency: int = 5,
    ) -> None:
        self.worker_id = worker_id
        self.queue_backend = queue_backend
        self.max_concurrency = max_concurrency
        self.active_jobs: int = 0
        self.hostname = socket.gethostname()
        self._handlers: dict[str, TaskHandler] = {}
        self._running = False
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._background_tasks: set[asyncio.Task[None]] = set()

    def register_handler(self, task_name: str, handler: TaskHandler) -> None:
        """Register an async handler for a task name."""
        self._handlers[task_name] = handler
        logger.info(f"Worker '{self.worker_id}' registered task handler: {task_name}")

    def get_heartbeat(self) -> WorkerHeartbeat:
        """Produce worker heartbeat and saturation status."""
        sat_pct = round((self.active_jobs / self.max_concurrency) * 100, 2)
        return WorkerHeartbeat(
            worker_id=self.worker_id,
            hostname=self.hostname,
            active_jobs=self.active_jobs,
            max_concurrency=self.max_concurrency,
            saturation_pct=sat_pct,
        )

    async def execute_one(self, wait_completion: bool = True) -> bool:
        """Fetch and execute one job from the queue if capacity allows."""
        if self.active_jobs >= self.max_concurrency:
            return False

        job = await self.queue_backend.dequeue()
        if not job:
            return False

        if wait_completion:
            await self._run_job(job)
        else:
            task = asyncio.create_task(self._run_job(job))
            self._background_tasks.add(task)
            task.add_done_callback(self._background_tasks.discard)
        return True

    async def _run_job(self, job: Job) -> None:
        async with self._semaphore:
            self.active_jobs += 1
            request_id_ctx.set(job.id)
            tenant_id_ctx.set(job.tenant_id)
            logger.info(
                f"Worker '{self.worker_id}' started job '{job.id}' [{job.task_name}]"
            )

            try:
                handler = self._handlers.get(job.task_name)
                if not handler:
                    raise ValueError(
                        f"No registered handler for task '{job.task_name}'"
                    )

                result = await handler(job.payload)
                await self.queue_backend.complete_job(job.id, result)
            except Exception as e:
                logger.error(f"Worker failed on job '{job.id}': {e}", exc_info=True)
                await self.queue_backend.fail_job(job.id, str(e), retry=True)
            finally:
                self.active_jobs -= 1
