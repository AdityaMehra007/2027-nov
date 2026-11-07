"""ATLAS deterministic intelligence baseline.

This module deliberately does not call a hosted model. It provides a reproducible
baseline and a provider boundary for later model-backed implementations.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
import re

SKILL_CATALOG = (
    "python", "sql", "excel", "power bi", "tableau", "communication",
    "stakeholder management", "project management", "data analysis",
    "process improvement", "reporting", "procurement", "operations",
    "financial analysis", "machine learning", "typescript", "java",
    "cloud", "aws", "azure", "customer service", "research", "automation",
)

@dataclass(frozen=True)
class JobAnalysisRequest:
    job_title: str
    job_description: str
    profile_evidence: tuple[str, ...]

@dataclass(frozen=True)
class SkillEvidence:
    skill: str
    matched: bool
    evidence: tuple[str, ...]

@dataclass(frozen=True)
class JobAnalysis:
    engine: str
    job_title: str
    extracted_requirements: tuple[str, ...]
    evidence_map: tuple[SkillEvidence, ...]
    unsupported_requirements: tuple[str, ...]
    disclaimer: str

class IntelligenceProvider(Protocol):
    def analyze_job(self, request: JobAnalysisRequest) -> JobAnalysis: ...

class DeterministicProvider:
    """Transparent keyword baseline; not semantic matching or an LLM."""
    def __init__(self, catalog: tuple[str, ...] = SKILL_CATALOG) -> None:
        self.catalog = tuple(sorted(set(catalog), key=len, reverse=True))

    @staticmethod
    def _normalise(text: str) -> str:
        return re.sub(r"\s+", " ", text.casefold()).strip()

    def analyze_job(self, request: JobAnalysisRequest) -> JobAnalysis:
        description = self._normalise(request.job_description)
        evidence = tuple(self._normalise(item) for item in request.profile_evidence if item.strip())
        requirements = tuple(skill for skill in self.catalog if skill in description)
        results: list[SkillEvidence] = []
        missing: list[str] = []
        for skill in requirements:
            proof = tuple(
                request.profile_evidence[i]
                for i, item in enumerate(evidence)
                if skill in item
            )
            results.append(SkillEvidence(skill=skill, matched=bool(proof), evidence=proof))
            if not proof:
                missing.append(skill)
        return JobAnalysis(
            engine="deterministic-keyword-baseline",
            job_title=request.job_title.strip(),
            extracted_requirements=requirements,
            evidence_map=tuple(results),
            unsupported_requirements=tuple(missing),
            disclaimer=("Keyword baseline only. It does not establish qualification, suitability or hiring probability. "
                        "Review the original job description and evidence manually."),
        )
