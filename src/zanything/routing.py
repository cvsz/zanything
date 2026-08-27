"""Intent routing — keyword-based mode selection and workflow generation.

This is a simple keyword matcher. It will be replaced by a real intent
classification system in later milestones.
"""

MODE_RULES: dict[str, list[str]] = {
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
    "PROJECT_EXECUTION": [
        "end-to-end",
        "do all",
        "project",
        "production",
        "enterprise-grade",
    ],
}


def route_modes(text: str) -> list[str]:
    """Return matching modes for the given objective text."""
    t = text.lower()
    selected = [mode for mode, keys in MODE_RULES.items() if any(k in t for k in keys)]
    return selected or ["GENERAL"]


def workflow_for(modes: list[str]) -> list[str]:
    """Generate a workflow step list for the given modes."""
    steps = ["UNDERSTAND", "CLASSIFY", "PLAN", "EXECUTE"]
    if any(
        m in modes
        for m in ["CODING", "DEBUGGING", "SECURITY", "DEVOPS_SRE", "PROJECT_EXECUTION"]
    ):
        steps += ["TEST", "HARDEN"]
    steps += ["VERIFY", "DELIVER"]
    return steps
