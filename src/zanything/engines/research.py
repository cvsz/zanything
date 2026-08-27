"""Deep Research Engine: Plan generation and Report rendering."""

import datetime

from pydantic import BaseModel, Field

from zanything.logging import get_logger

logger = get_logger("zanything.engines.research")


class ResearchSource(BaseModel):
    """Evaluated information source with authority and freshness scoring."""

    url: str
    title: str
    authority_score: float = Field(
        ge=0.0, le=1.0, description="Source trustworthiness (0-1)"
    )
    freshness_score: float = Field(ge=0.0, le=1.0, description="Freshness (0-1)")
    is_primary: bool = False
    excerpt: str


class ResearchFinding(BaseModel):
    """Individual synthesized finding backed by citation evidence."""

    claim: str
    confidence_score: float
    sources: list[str]
    contradictions_detected: list[str] = Field(default_factory=list)


class DeepResearchReport(BaseModel):
    """Structured research report with evidence graph and citation integrity."""

    topic: str
    tenant_id: str
    summary: str
    findings: list[ResearchFinding]
    sources: list[ResearchSource]
    overall_confidence: float
    generated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )


class DeepResearchEngine:
    """Executes multi-step deep research workflows with source authority."""

    def analyze_and_synthesize(
        self, topic: str, raw_sources: list[ResearchSource], tenant_id: str
    ) -> DeepResearchReport:
        """Synthesize evaluated sources into citation-backed research report."""
        logger.info(
            f"Synthesizing deep research for '{topic}' from {len(raw_sources)} sources"
        )

        # Deduplicate and sort by authority
        unique_sources = {s.url: s for s in raw_sources}.values()
        sorted_sources = sorted(
            unique_sources,
            key=lambda s: (s.is_primary, s.authority_score),
            reverse=True,
        )

        findings: list[ResearchFinding] = []
        if sorted_sources:
            primary_src = sorted_sources[0]
            findings.append(
                ResearchFinding(
                    claim=(
                        f"Primary findings on {topic} established "
                        f"from {primary_src.title}."
                    ),
                    confidence_score=primary_src.authority_score,
                    sources=[primary_src.url],
                )
            )

        avg_conf = (
            sum(s.authority_score for s in sorted_sources) / len(sorted_sources)
            if sorted_sources
            else 0.5
        )

        return DeepResearchReport(
            topic=topic,
            tenant_id=tenant_id,
            summary=f"Deep research synthesis for topic '{topic}'.",
            findings=findings,
            sources=list(sorted_sources),
            overall_confidence=round(avg_conf, 2),
        )
