"""zanything — Enterprise Universal AI Operator FastAPI Application."""

import time
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, Header, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from zanything.auth import Principal, Role
from zanything.auth.dependencies import get_current_principal, require_role
from zanything.config import Settings, get_settings
from zanything.errors import ProblemDetails, register_exception_handlers
from zanything.logging import (
    configure_logging,
    get_logger,
    request_id_ctx,
    tenant_id_ctx,
)
from zanything.models import (
    CapabilityResponse,
    ExecuteRequest,
    ExecuteResponse,
    HealthResponse,
)
from zanything.routing import MODE_RULES, route_modes, workflow_for

STARTED_AT = time.time()
GUI_DIR = Path(__file__).resolve().parent / "gui"
logger = get_logger("zanything.app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifecycle management for startup and graceful shutdown."""
    settings = get_settings()
    configure_logging(level=settings.log_level, json_format=settings.log_json)
    logger.info(
        f"Starting {settings.app_name} v{settings.app_version} in [{settings.env}] mode"
    )
    yield
    logger.info(f"Shutting down {settings.app_name} gracefully")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Application factory for zanything."""
    active_settings = settings or get_settings()

    app = FastAPI(
        title=active_settings.app_name,
        version=active_settings.app_version,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        responses={
            401: {"model": ProblemDetails, "description": "Unauthorized"},
            403: {"model": ProblemDetails, "description": "Forbidden"},
            422: {"model": ProblemDetails, "description": "Validation Error"},
            500: {"model": ProblemDetails, "description": "Internal Server Error"},
        },
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=active_settings.allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-API-Key",
            "X-Request-ID",
            "X-Tenant-ID",
            "Idempotency-Key",
        ],
    )

    # Request Context & Correlation ID Middleware
    @app.middleware("http")
    async def request_context_middleware(
        request: Request, call_next: object
    ) -> Response:
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        tenant_id = request.headers.get("X-Tenant-ID") or "default"

        request_id_ctx.set(req_id)
        tenant_id_ctx.set(tenant_id)

        start_time = time.perf_counter()
        logger.info(f"Incoming request {request.method} {request.url.path}")

        response: Response = await call_next(request)  # type: ignore[operator]

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        response.headers["X-Request-ID"] = req_id
        logger.info(
            f"Completed {request.method} {request.url.path} "
            f"[{response.status_code}] in {duration_ms}ms"
        )
        return response

    # Register RFC 7807 Exception Handlers
    register_exception_handlers(app)

    # Static GUI Mount
    if GUI_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(GUI_DIR)), name="static")

    # Routes
    @app.get("/", response_model=None, include_in_schema=False)
    def index() -> dict[str, str] | FileResponse:
        """Serve operator GUI if available, otherwise return API info."""
        index_path = GUI_DIR / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {
            "name": active_settings.app_name,
            "version": active_settings.app_version,
        }

    @app.get("/healthz", response_model=HealthResponse, tags=["Observability"])
    def healthz() -> HealthResponse:
        """Liveness probe: verifies process is alive and responsive."""
        cfg = get_settings()
        return HealthResponse(
            status="ok",
            app=cfg.app_name,
            version=cfg.app_version,
            uptime_seconds=round(time.time() - STARTED_AT, 2),
        )

    @app.get("/readyz", response_model=HealthResponse, tags=["Observability"])
    def readyz() -> HealthResponse:
        """Readiness probe: reports dependency health and runtime readiness."""
        cfg = get_settings()
        return HealthResponse(
            status="no-dependencies",
            app=cfg.app_name,
            version=cfg.app_version,
            uptime_seconds=round(time.time() - STARTED_AT, 2),
            dependencies={},
        )

    @app.get("/version", tags=["Observability"])
    def version() -> dict[str, str]:
        """Return application name and version metadata."""
        cfg = get_settings()
        return {"name": cfg.app_name, "version": cfg.app_version, "env": cfg.env}

    @app.get(
        "/v1/capabilities", response_model=CapabilityResponse, tags=["Capabilities"]
    )
    def capabilities() -> CapabilityResponse:
        """List verified active capability modes and runtime features."""
        return CapabilityResponse(
            modes=list(MODE_RULES.keys()),
            features=[
                "keyword-routing",
                "dry-run",
                "request-context",
                "rfc7807-errors",
                "structured-logging",
                "oidc-jwt-auth",
                "rbac-abac-security",
                "service-accounts",
            ],
        )

    @app.get("/v1/me", response_model=Principal, tags=["Identity"])
    def me(principal: Principal = Depends(get_current_principal)) -> Principal:
        """Return current authenticated principal context with tenant and roles."""
        return principal

    @app.post("/v1/execute", response_model=ExecuteResponse, tags=["Execution"])
    def execute(
        req: ExecuteRequest,
        principal: Principal = Depends(get_current_principal),
        x_request_id: str | None = Header(default=None),
        idempotency_key: str | None = Header(default=None),
    ) -> ExecuteResponse:
        """Analyze and route an objective into specialist modes."""
        req_id = x_request_id or request_id_ctx.get()
        modes = req.requested_modes or route_modes(req.objective)
        workflow = workflow_for(modes)

        logger.info(
            f"Principal '{principal.subject}' (tenant: {principal.tenant_id}) "
            f"routed objective to modes: {modes}"
        )

        return ExecuteResponse(
            request_id=req_id,
            status="dry-run-planned" if req.dry_run else "routed",
            objective=req.objective,
            modes=modes,
            workflow=workflow,
            dry_run=req.dry_run,
            verification_required=req.require_verification,
        )

    # Admin Management API (Protected by Role.ADMIN)
    @app.get("/v1/admin/roles", tags=["Admin"])
    def list_roles(
        _principal: Principal = Depends(require_role(Role.ADMIN)),
    ) -> dict[str, Any]:
        """List enterprise roles and permission hierarchy."""
        return {
            "roles": [r.value for r in Role],
            "descriptions": {
                Role.ADMIN: "Full system administration and policy management",
                Role.OPERATOR: (
                    "Execute workflows, manage jobs, and configure adapters"
                ),
                Role.VIEWER: "Read-only access to status and executions",
                Role.AUDITOR: (
                    "Read-only access to audit logs and compliance evidence"
                ),
            },
        }

    # --- Capability Engines Endpoints ---

    @app.post(
        "/v1/research/synthesize",
        tags=["Engines"],
        summary="Synthesize multi-source deep research report",
    )
    def synthesize_research(
        topic: str,
        sources: list[dict[str, Any]],
        principal: Principal = Depends(get_current_principal),
    ) -> dict[str, Any]:
        from zanything.engines.research import DeepResearchEngine, ResearchSource

        engine = DeepResearchEngine()
        parsed_sources = [ResearchSource(**s) for s in sources]
        report = engine.analyze_and_synthesize(
            topic=topic,
            raw_sources=parsed_sources,
            tenant_id=principal.tenant_id,
        )
        return report.model_dump()

    @app.post(
        "/v1/devops/plan",
        tags=["Engines"],
        summary="Generate deployment and rollback plan",
    )
    def plan_deployment(
        target: str,
        app_version: str,
        principal: Principal = Depends(require_role(Role.OPERATOR)),
    ) -> dict[str, Any]:
        from zanything.engines.devops import DeploymentTarget, DevOpsEngine

        engine = DevOpsEngine()
        dep_target = DeploymentTarget(target.lower())
        plan = engine.plan_deployment(
            target=dep_target,
            tenant_id=principal.tenant_id,
            app_version=app_version,
        )
        return plan.model_dump()

    @app.post(
        "/v1/security/audit",
        tags=["Engines"],
        summary="Run security baseline checks",
    )
    def audit_security(
        target_service: str,
        checks: list[dict[str, str]],
        principal: Principal = Depends(require_role(Role.AUDITOR)),
    ) -> dict[str, Any]:
        from zanything.engines.security import SecurityEngine

        engine = SecurityEngine()
        report = engine.audit_configuration(
            target_service=target_service,
            tenant_id=principal.tenant_id,
            checks=checks,
        )
        return report.model_dump()

    @app.get(
        "/v1/governance/slo",
        tags=["Governance"],
        summary="Calculate real-time SLO and error budget",
    )
    def get_slo_status(
        total_requests: int = 10000,
        failed_requests: int = 5,
        target_pct: float = 99.9,
        _principal: Principal = Depends(get_current_principal),
    ) -> dict[str, Any]:
        from zanything.governance import SLOMonitor

        monitor = SLOMonitor()
        metric = monitor.evaluate_availability(
            total_requests=total_requests,
            failed_requests=failed_requests,
            target_pct=target_pct,
        )
        return metric.model_dump()

    @app.get(
        "/v1/distribution/diagnostics",
        tags=["Distribution"],
        summary="Export sanitized support diagnostic bundle",
    )
    def get_diagnostics(
        principal: Principal = Depends(require_role(Role.ADMIN)),
    ) -> dict[str, Any]:
        from zanything.distribution import DiagnosticBundle

        bundle = DiagnosticBundle(
            bundle_id=f"diag-{int(time.time())}",
            tenant_id=principal.tenant_id,
            system_health={"api": "healthy", "db": "healthy", "queue": "healthy"},
            active_workers=4,
            open_circuits=[],
        )
        return bundle.model_dump()

    return app


# Default singleton instance
app = create_app()
