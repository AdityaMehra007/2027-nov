# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""PROJECT GODMODE / ATLAS: Career OS REST API Router."""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from omniverse.modules.career.engine import CareerOSEngine
from omniverse.modules.career.models import (
    CandidateProfile,
    JobOpportunity,
    OpportunityStatus,
    JobDescriptionAnalysis,
    TailoredResume,
    OutreachDraft,
    InterviewPrepPack,
    ActionApproval,
    ApprovalStatus,
)

_career_engine = CareerOSEngine()


def get_career_engine() -> CareerOSEngine:
    return _career_engine


class AddOpportunityRequest(BaseModel):
    company: str
    role_title: str
    location: str
    source_url: str
    salary_range: str = "Market Competitive"
    jd_raw_text: str = ""
    notes: str = ""


class StatusUpdateRequest(BaseModel):
    status: OpportunityStatus


class ApprovalDecisionRequest(BaseModel):
    approved: bool


def get_career_router() -> APIRouter:
    router = APIRouter(prefix="/career", tags=["Career OS"])

    @router.get("/profile", response_model=CandidateProfile)
    def get_profile() -> CandidateProfile:
        return _career_engine.get_profile()

    @router.put("/profile", response_model=CandidateProfile)
    def update_profile(profile: CandidateProfile) -> CandidateProfile:
        return _career_engine.update_profile(profile)

    @router.get("/opportunities", response_model=List[JobOpportunity])
    def list_opportunities(status: Optional[OpportunityStatus] = None) -> List[JobOpportunity]:
        return _career_engine.list_opportunities(status=status)

    @router.post("/opportunities", response_model=JobOpportunity)
    def add_opportunity(req: AddOpportunityRequest) -> JobOpportunity:
        opp = JobOpportunity(
            company=req.company,
            role_title=req.role_title,
            location=req.location,
            source_url=req.source_url,
            salary_range=req.salary_range,
            jd_raw_text=req.jd_raw_text,
            notes=req.notes
        )
        return _career_engine.add_opportunity(opp)

    @router.get("/opportunities/{opp_id}", response_model=JobOpportunity)
    def get_opportunity(opp_id: str) -> JobOpportunity:
        opp = _career_engine.get_opportunity(opp_id)
        if not opp:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        return opp

    @router.patch("/opportunities/{opp_id}/status", response_model=JobOpportunity)
    def update_status(opp_id: str, req: StatusUpdateRequest) -> JobOpportunity:
        try:
            return _career_engine.update_opportunity_status(opp_id, req.status)
        except KeyError:
            raise HTTPException(status_code=404, detail="Opportunity not found")

    @router.post("/opportunities/{opp_id}/analyze", response_model=JobDescriptionAnalysis)
    def analyze_jd(opp_id: str, jd_text: Optional[str] = Query(None)) -> JobDescriptionAnalysis:
        try:
            return _career_engine.analyze_job_description(opp_id, jd_text)
        except KeyError:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))

    @router.post("/opportunities/{opp_id}/tailor-resume", response_model=TailoredResume)
    def tailor_resume(opp_id: str) -> TailoredResume:
        try:
            return _career_engine.tailor_resume(opp_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Opportunity not found")

    @router.post("/opportunities/{opp_id}/outreach", response_model=OutreachDraft)
    def generate_outreach(opp_id: str, channel: str = Query("EMAIL"), recipient_role: str = Query("Hiring Director")) -> OutreachDraft:
        try:
            return _career_engine.generate_outreach_draft(opp_id, channel=channel, recipient_role=recipient_role)
        except KeyError:
            raise HTTPException(status_code=404, detail="Opportunity not found")

    @router.post("/opportunities/{opp_id}/interview-pack", response_model=InterviewPrepPack)
    def generate_interview_pack(opp_id: str) -> InterviewPrepPack:
        try:
            return _career_engine.generate_interview_prep(opp_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Opportunity not found")

    @router.get("/approvals", response_model=List[ActionApproval])
    def list_approvals(status: Optional[ApprovalStatus] = None) -> List[ActionApproval]:
        return _career_engine.list_approvals(status=status)

    @router.post("/approvals/{appr_id}/decide", response_model=ActionApproval)
    def decide_approval(appr_id: str, req: ApprovalDecisionRequest) -> ActionApproval:
        try:
            return _career_engine.decide_approval(appr_id, req.approved)
        except KeyError:
            raise HTTPException(status_code=404, detail="Approval request not found")

    @router.get("/export")
    def export_dossier() -> Dict[str, Any]:
        return _career_engine.export_career_dossier()

    return router
