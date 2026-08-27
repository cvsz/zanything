"""Tests for v6 Durable Data Runtime (Repositories & Tenant Isolation)."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from zanything.db import Base
from zanything.db.repositories import (
    AuditRepository,
    IdempotencyRepository,
    TaskRepository,
)


@pytest.fixture
async def async_session() -> AsyncSession:
    """In-memory async SQLite engine fixture for repository integration tests."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with session_maker() as session:
        yield session

    await engine.dispose()


@pytest.mark.anyio
async def test_task_creation_and_retrieval(async_session: AsyncSession) -> None:
    """Create task and retrieve with strict tenant boundary."""
    repo_tenant_a = TaskRepository(async_session, tenant_id="tenant-alpha")
    task = await repo_tenant_a.create_task(
        task_id="task-001",
        subject="alice",
        objective="Run security audit",
        modes=["SECURITY"],
        workflow=["UNDERSTAND", "PLAN", "EXECUTE", "VERIFY"],
    )
    assert task.id == "task-001"
    assert task.tenant_id == "tenant-alpha"

    # Verify retrieval within same tenant
    fetched = await repo_tenant_a.get_task("task-001")
    assert fetched is not None
    assert fetched.objective == "Run security audit"

    # Verify tenant isolation: tenant-beta must NOT be able to see task-001
    repo_tenant_b = TaskRepository(async_session, tenant_id="tenant-beta")
    foreign_task = await repo_tenant_b.get_task("task-001")
    assert foreign_task is None


@pytest.mark.anyio
async def test_idempotency_key_persistence(async_session: AsyncSession) -> None:
    """Record and retrieve idempotency responses per tenant."""
    repo = IdempotencyRepository(async_session, tenant_id="tenant-fintech")
    await repo.record_response(
        key="idemp-key-xyz",
        request_id="req-123",
        endpoint="/v1/execute",
        status_code=200,
        response_payload={"status": "routed", "modes": ["CODING"]},
    )

    recorded = await repo.get_recorded_response("idemp-key-xyz")
    assert recorded is not None
    assert recorded.status_code == 200
    assert recorded.response_payload["status"] == "routed"

    # Other tenant cannot access idempotency key
    repo_other = IdempotencyRepository(async_session, tenant_id="tenant-other")
    assert await repo_other.get_recorded_response("idemp-key-xyz") is None


@pytest.mark.anyio
async def test_audit_event_logging(async_session: AsyncSession) -> None:
    """Append audit trail event and list per tenant."""
    repo = AuditRepository(async_session, tenant_id="tenant-audit-corp")
    await repo.record_event(
        actor_id="admin-user",
        actor_type="user",
        action="UPDATE_ROLE",
        resource_type="ROLE",
        resource_id="operator",
        status="SUCCESS",
        request_id="req-audit-1",
        details={"previous": "viewer", "new": "operator"},
    )

    events = await repo.list_events()
    assert len(events) == 1
    assert events[0].action == "UPDATE_ROLE"
    assert events[0].actor_id == "admin-user"
    assert events[0].tenant_id == "tenant-audit-corp"
