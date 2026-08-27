
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

APP_NAME = "Anything Enterprise Universal Operator"
APP_VERSION = "3.0.0"
STARTED = time.time()
ROOT = Path(__file__).resolve().parent.parent
GUI_DIR = ROOT / "gui"

app = FastAPI(title=APP_NAME, version=APP_VERSION)

origins = [x.strip() for x in os.getenv("ANYTHING_ALLOWED_ORIGINS", "http://localhost:8080").split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Request-ID", "Idempotency-Key"],
)

if GUI_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(GUI_DIR)), name="static")

class ExecuteRequest(BaseModel):
    objective: str = Field(min_length=1, max_length=20000)
    context: Dict[str, Any] = Field(default_factory=dict)
    requested_modes: List[str] = Field(default_factory=list)
    dry_run: bool = False
    require_verification: bool = True

class ExecuteResponse(BaseModel):
    request_id: str
    status: str
    objective: str
    modes: List[str]
    workflow: List[str]
    dry_run: bool
    verification_required: bool

MODE_RULES = {
    "RESEARCH": ["research", "find", "source", "compare", "latest"],
    "DEEP_RESEARCH": ["deep research", "deep dive", "comprehensive research"],
    "CODING": ["code", "implement", "build", "refactor", "repository", "repo"],
    "DEBUGGING": ["debug", "bug", "error", "failing", "failure"],
    "ARCHITECTURE": ["architecture", "system design", "platform design"],
    "SECURITY": ["security", "secure", "audit", "vulnerability", "threat model"],
    "DEVOPS_SRE": ["devops", "sre", "docker", "kubernetes", "helm", "ci/cd", "deploy"],
    "DATA": ["data", "csv", "xlsx", "statistics", "analytics"],
    "DOCUMENTS": ["document", "report", "sop", "policy", "proposal"],
    "SPREADSHEETS": ["spreadsheet", "workbook", "xlsx", "excel"],
    "PRESENTATIONS": ["presentation", "slides", "pptx", "deck"],
    "IMAGES": ["image", "visual", "artwork", "generate image"],
    "MOVIE_POSTERS": ["movie poster", "poster", "key art"],
    "UI_UX": ["ui", "ux", "interface", "design system", "wireframe"],
    "MARKETING": ["marketing", "seo", "campaign", "content strategy"],
    "BUSINESS": ["business", "strategy", "market", "pricing"],
    "AUTOMATION": ["automation", "automate", "workflow", "integration"],
    "DECISION_MAKING": ["decision", "choose", "best option", "recommend"],
    "MULTIMODAL": ["multimodal", "files", "images and text", "cross-file"],
    "PROJECT_EXECUTION": ["end-to-end", "do all", "project", "production", "enterprise-grade"],
}

def route_modes(text: str) -> List[str]:
    t = text.lower()
    selected = []
    for mode, keys in MODE_RULES.items():
        if any(k in t for k in keys):
            selected.append(mode)
    return selected or ["GENERAL"]

def workflow_for(modes: List[str]) -> List[str]:
    steps = ["UNDERSTAND", "CLASSIFY", "PLAN", "EXECUTE"]
    if any(m in modes for m in ["CODING","DEBUGGING","SECURITY","DEVOPS_SRE","PROJECT_EXECUTION"]):
        steps += ["TEST", "HARDEN"]
    steps += ["VERIFY", "DELIVER"]
    return steps

@app.get("/")
def index():
    p = GUI_DIR / "index.html"
    if p.exists():
        return FileResponse(str(p))
    return {"name": APP_NAME, "version": APP_VERSION}

@app.get("/healthz")
def healthz():
    return {"status":"ok"}

@app.get("/readyz")
def readyz():
    return {"status":"ready","uptime_seconds":round(time.time()-STARTED,2)}

@app.get("/version")
def version():
    return {"name":APP_NAME,"version":APP_VERSION}

@app.get("/v1/capabilities")
def capabilities():
    return {
        "modes": list(MODE_RULES.keys()),
        "features": [
            "universal-routing","dry-run","verification-gates","integration-ready",
            "enterprise-gui","request-ids","idempotency-header-ready"
        ]
    }

@app.post("/v1/execute", response_model=ExecuteResponse)
def execute(
    req: ExecuteRequest,
    x_request_id: Optional[str] = Header(default=None),
    idempotency_key: Optional[str] = Header(default=None),
):
    request_id = x_request_id or str(uuid.uuid4())
    modes = req.requested_modes or route_modes(req.objective)
    return ExecuteResponse(
        request_id=request_id,
        status="planned" if req.dry_run else "accepted",
        objective=req.objective,
        modes=modes,
        workflow=workflow_for(modes),
        dry_run=req.dry_run,
        verification_required=req.require_verification,
    )
