"""Tenant-scoped async repositories enforcing query boundaries."""

from typing import Any

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from zanything.db.models import AuditEventModel, IdempotencyKeyModel, TaskModel


class TenantScopedRepository:
    """Base repository ensuring all operations are scoped to a tenant."""

    def __init__(self, session: AsyncSession, tenant_id: str) -> None:
        self.session = session
        self.tenant_id = tenant_id


class TaskRepository(TenantScopedRepository):
    """Repository for Task persistence with strict tenant isolation."""

    async def create_task(
        self,
        task_id: str,
        subject: str,
        objective: str,
        modes: list[str],
        workflow: list[str],
        dry_run: bool = False,
        verification_required: bool = True,
        context_data: dict[str, Any] | None = None,
    ) -> TaskModel:
        task = TaskModel(
            id=task_id,
            tenant_id=self.tenant_id,
            subject=subject,
            objective=objective,
            status="dry-run-planned" if dry_run else "routed",
            modes=modes,
            workflow=workflow,
            dry_run=dry_run,
            verification_required=verification_required,
            context_data=context_data or {},
        )
        self.session.add(task)
        await self.session.flush()
        return task

    async def get_task(self, task_id: str) -> TaskModel | None:
        """Get task strictly isolated by tenant."""
        stmt = select(TaskModel).where(
            TaskModel.id == task_id, TaskModel.tenant_id == self.tenant_id
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_tasks(self, limit: int = 50, offset: int = 0) -> list[TaskModel]:
        """List tasks for the current tenant ordered by creation time."""
        stmt = (
            select(TaskModel)
            .where(TaskModel.tenant_id == self.tenant_id)
            .order_by(desc(TaskModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())


class IdempotencyRepository(TenantScopedRepository):
    """Repository managing request idempotency records."""

    async def get_recorded_response(self, key: str) -> IdempotencyKeyModel | None:
        stmt = select(IdempotencyKeyModel).where(
            IdempotencyKeyModel.key == key,
            IdempotencyKeyModel.tenant_id == self.tenant_id,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def record_response(
        self,
        key: str,
        request_id: str,
        endpoint: str,
        status_code: int,
        response_payload: dict[str, Any],
    ) -> IdempotencyKeyModel:
        record = IdempotencyKeyModel(
            key=key,
            tenant_id=self.tenant_id,
            request_id=request_id,
            endpoint=endpoint,
            status_code=status_code,
            response_payload=response_payload,
        )
        self.session.add(record)
        await self.session.flush()
        return record


class AuditRepository(TenantScopedRepository):
    """Repository for appending and querying tenant audit logs."""

    async def record_event(
        self,
        actor_id: str,
        actor_type: str,
        action: str,
        resource_type: str,
        status: str,
        request_id: str,
        resource_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> AuditEventModel:
        event = AuditEventModel(
            tenant_id=self.tenant_id,
            actor_id=actor_id,
            actor_type=actor_type,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            request_id=request_id,
            details=details or {},
        )
        self.session.add(event)
        await self.session.flush()
        return event

    async def list_events(
        self, limit: int = 100, offset: int = 0
    ) -> list[AuditEventModel]:
        stmt = (
            select(AuditEventModel)
            .where(AuditEventModel.tenant_id == self.tenant_id)
            .order_by(desc(AuditEventModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
