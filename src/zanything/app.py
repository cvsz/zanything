"""zanything — FastAPI application.

This is the main application entry point. Currently implements:
- Keyword-based intent routing (no real execution)
- Health check (basic, no dependency verification)
- Capability listing (honest about current state)
"""

import os
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from zanything.models import ExecuteRequest, ExecuteResponse
from zanything.routing import MODE_RULES, route_modes, workflow_for

APP_NAME = "zanything"
APP_VERSION = "0.1.0"
STARTED = time.time()

# GUI directory is adjacent to this file
GUI_DIR = Path(__file__).resolve().parent / "gui"

app = FastAPI(title=APP_NAME, version=APP_VERSION)

origins = [
    x.strip()
    for x in os.getenv("ZANYTHING_ALLOWED_ORIGINS", "http://localhost:8080").split(",")
    if x.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Request-ID", "Idempotency-Key"],
)

if GUI_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(GUI_DIR)), name="static")


@app.get("/", response_model=None)
def index() -> dict[str, str] | FileResponse:
    """Serve GUI if available, otherwise return service info."""
    p = GUI_DIR / "index.html"
    if p.exists():
        return FileResponse(str(p))
    return {"name": APP_NAME, "version": APP_VERSION}


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Basic liveness probe. Does not verify dependencies."""
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, object]:
    """Readiness probe.

    Currently only reports uptime. Real dependency checks (database,
    queue, providers) will be added as those dependencies are implemented.
    """
    return {
        "status": "no-dependencies",
        "uptime_seconds": round(time.time() - STARTED, 2),
    }


@app.get("/version")
def version() -> dict[str, str]:
    """Return service name and version."""
    return {"name": APP_NAME, "version": APP_VERSION}


@app.get("/v1/capabilities")
def capabilities() -> dict[str, object]:
    """List available routing modes and implemented features."""
    return {
        "modes": list(MODE_RULES.keys()),
        "features": [
            "keyword-routing",
            "dry-run",
            "request-ids",
        ],
    }


@app.post("/v1/execute", response_model=ExecuteResponse)
def execute(
    req: ExecuteRequest,
    x_request_id: str | None = Header(default=None),
    idempotency_key: str | None = Header(default=None),
) -> ExecuteResponse:
    """Route an objective to modes and generate a workflow plan.

    This endpoint currently performs keyword-based routing only.
    No actual execution, queuing, or processing occurs.
    """
    request_id = x_request_id or str(uuid.uuid4())
    modes = req.requested_modes or route_modes(req.objective)
    return ExecuteResponse(
        request_id=request_id,
        status="dry-run-planned" if req.dry_run else "routed",
        objective=req.objective,
        modes=modes,
        workflow=workflow_for(modes),
        dry_run=req.dry_run,
        verification_required=req.require_verification,
    )
