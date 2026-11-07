# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""PROJECT GODMODE / ATLAS: Career OS Data Models.

Encodes the verifiable career profile, opportunity pipeline, factual resume tailoring,
and human-in-the-loop approval entities.
"""

from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class OpportunityStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    RESEARCHING = "RESEARCHING"
    APPLIED = "APPLIED"
    INTERVIEWING = "INTERVIEWING"
    OFFERED = "OFFERED"
    REJECTED = "REJECTED"


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class VerifiedAchievement(BaseModel):
    id: str = Field(default_factory=lambda: f"ach_{uuid.uuid4().hex[:8]}")
    title: str
    impact_metric: str  # e.g., "Scaled revenue from $0 to $1M" or "Reduced p99 latency by 45%"
    skills_used: List[str] = Field(default_factory=list)
    evidence_url: Optional[str] = None
    created_at: float = Field(default_factory=time.time)


class CandidateProfile(BaseModel):
    user_id: str = "founder_default"
    full_name: str
    headline: str
    summary: str
    skills: List[str] = Field(default_factory=list)
    achievements: List[VerifiedAchievement] = Field(default_factory=list)
    target_roles: List[str] = Field(default_factory=list)
    target_compensation_min_usd: float = 150000.0
    preferred_locations: List[str] = Field(default_factory=lambda: ["Bengaluru", "Remote Global"])
    updated_at: float = Field(default_factory=time.time)


class JobOpportunity(BaseModel):
    id: str = Field(default_factory=lambda: f"opp_{uuid.uuid4().hex[:8]}")
    company: str
    role_title: str
    location: str
    source_url: str
    salary_range: str = "Market Competitive"
    status: OpportunityStatus = OpportunityStatus.DISCOVERED
    jd_raw_text: str = ""
    notes: str = ""
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class JobDescriptionAnalysis(BaseModel):
    opportunity_id: str
    extracted_requirements: List[str]
    match_score_pct: float
    matched_skills: List[str]
    skill_gaps: List[str]
    suggested_interview_questions: List[str]
    analyzed_at: float = Field(default_factory=time.time)


class TailoredResumeBullet(BaseModel):
    requirement: str
    bullet_point: str
    backed_by_achievement_id: str
    factually_verified: bool = True


class TailoredResume(BaseModel):
    id: str = Field(default_factory=lambda: f"res_{uuid.uuid4().hex[:8]}")
    opportunity_id: str
    target_role: str
    company: str
    tailored_headline: str
    tailored_summary: str
    aligned_bullets: List[TailoredResumeBullet]
    skills_highlighted: List[str]
    created_at: float = Field(default_factory=time.time)


class OutreachDraft(BaseModel):
    id: str = Field(default_factory=lambda: f"out_{uuid.uuid4().hex[:8]}")
    opportunity_id: str
    channel: str = "EMAIL"  # EMAIL or LINKEDIN
    recipient_role: str  # e.g., "Engineering Director", "Recruiter"
    subject: str
    body: str
    human_approved: bool = False
    created_at: float = Field(default_factory=time.time)


class STARQuestionResponse(BaseModel):
    question: str
    situation: str
    task: str
    action: str
    result: str
    evidence_achievement_id: str


class InterviewPrepPack(BaseModel):
    opportunity_id: str
    company: str
    role_title: str
    technical_focus_areas: List[str]
    behavioral_star_frameworks: List[STARQuestionResponse]
    company_reverse_interview_questions: List[str]
    generated_at: float = Field(default_factory=time.time)


class ActionApproval(BaseModel):
    id: str = Field(default_factory=lambda: f"appr_{uuid.uuid4().hex[:8]}")
    action_type: str  # SEND_OUTREACH, SUBMIT_APPLICATION, PUBLISH_PORTFOLIO
    description: str
    target_entity_id: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    status: ApprovalStatus = ApprovalStatus.PENDING
    requested_at: float = Field(default_factory=time.time)
    decided_at: Optional[float] = None
