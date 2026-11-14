"""
ATLAS NEXUS: Command Center & Project Intake
Natural language intent parsing, capability routing, and directive synthesis.
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Set

from src.nexus.departments import (
    CapabilityDescriptor,
    CapabilityRegistry,
    DepartmentEnum,
    get_all_capabilities,
    get_capability_by_id,
)


@dataclass
class ProjectDirective:
    directive_id: str
    raw_input: str
    user_id: str
    intent: str
    target_departments: List[DepartmentEnum]
    requested_capabilities: List[int]
    priority: str = "NORMAL"
    timestamp_hlc: int = field(default_factory=lambda: int(time.time() * 1000))


class NexusCommandCenter:
    def __init__(self, registry: Optional[CapabilityRegistry] = None) -> None:
        self.registry = registry or CapabilityRegistry()
        self._hlc_counter = 0

    def _next_hlc(self) -> int:
        self._hlc_counter += 1
        return int(time.time() * 1000) * 1000 + (self._hlc_counter % 1000)

    def parse_intake(
        self,
        raw_input: str,
        user_id: str = "aditya",
        priority: str = "NORMAL",
    ) -> ProjectDirective:
        if not raw_input or not raw_input.strip():
            raise ValueError("Input directive cannot be empty")

        cleaned = raw_input.strip().lower()
        directive_id = f"DIR-{uuid.uuid4().hex[:8].upper()}"

        departments: Set[DepartmentEnum] = set()
        capabilities: Set[int] = set()
        intent = "GENERAL_INTELLIGENCE"

        # Check for civilization-scale omnibus keywords
        omnibus_keywords = ["everything", "omniverse", "civilization", "all time", "biggest", "frontier project", "atlas nexus"]
        if any(kw in cleaned for kw in omnibus_keywords):
            intent = "CIVILIZATION_SCALE_OMNIVERSE"
            for d in DepartmentEnum:
                departments.add(d)
            for c in self.registry.get_all():
                capabilities.add(c.id)
            return ProjectDirective(
                directive_id=directive_id,
                raw_input=raw_input,
                user_id=user_id,
                intent=intent,
                target_departments=list(departments),
                requested_capabilities=sorted(list(capabilities)),
                priority=priority,
                timestamp_hlc=self._next_hlc(),
            )

        # Department A: Universal Intelligence & Research
        if any(w in cleaned for w in ["research", "paper", "knowledge", "university", "citation", "verify", "claim"]):
            departments.add(DepartmentEnum.DEPT_A)
            capabilities.update([1, 2, 3, 5])
            intent = "RESEARCH_AND_SYNTHESIS"

        # Department B: Science & Frontier Technology
        if any(w in cleaned for w in ["quantum", "physics", "robot", "biotech", "plasma", "materials", "fusion", "orbit", "space", "climate", "medical"]):
            departments.add(DepartmentEnum.DEPT_B)
            if "quantum" in cleaned:
                capabilities.add(8)
            if "robot" in cleaned:
                capabilities.add(7)
            if "plasma" in cleaned or "energy" in cleaned:
                capabilities.add(11)
            if "space" in cleaned or "orbit" in cleaned:
                capabilities.add(12)
            if "climate" in cleaned:
                capabilities.add(13)
            if "biotech" in cleaned or "medical" in cleaned:
                capabilities.update([9, 14])
            if not capabilities.intersection(range(6, 16)):
                capabilities.update([6, 15])
            intent = "SCIENTIFIC_FRONTIER_EXPERIMENTATION"

        # Department C: Computational & Engineering Systems
        if any(w in cleaned for w in ["simulation", "digital twin", "data engineering", "iot", "hardware", "verilog", "autograd"]):
            departments.add(DepartmentEnum.DEPT_C)
            capabilities.update([16, 17, 20])
            intent = "ENGINEERING_SIMULATION"

        # Department D: Business & Economic Intelligence
        if any(w in cleaned for w in ["finance", "trading", "ledger", "stock", "market", "startup", "economy", "book", "order"]):
            departments.add(DepartmentEnum.DEPT_D)
            capabilities.update([21, 22, 23, 24])
            intent = "QUANTITATIVE_FINANCE_AND_BUSINESS"

        # Department E: Human Knowledge & Education
        if any(w in cleaned for w in ["education", "career", "interview", "media", "productivity", "crdt", "wiki"]):
            departments.add(DepartmentEnum.DEPT_E)
            capabilities.update([26, 27, 28, 30])
            intent = "HUMAN_KNOWLEDGE_AND_EDUCATION"

        # Department F: World & Infrastructure
        if any(w in cleaned for w in ["city", "urban", "traffic", "agriculture", "food", "supply chain", "geospatial", "satellite"]):
            departments.add(DepartmentEnum.DEPT_F)
            capabilities.update([31, 32, 33, 34, 35])
            intent = "INFRASTRUCTURE_AND_WORLD_SYSTEMS"

        # Department G: Creation & Execution (Software Factory)
        if any(w in cleaned for w in ["saas", "software", "code", "app", "application", "factory", "generate", "build", "foundry", "agent"]):
            departments.add(DepartmentEnum.DEPT_G)
            departments.add(DepartmentEnum.DEPT_C)
            capabilities.update([18, 36, 37, 40])
            if intent == "GENERAL_INTELLIGENCE":
                intent = "AUTONOMOUS_SOFTWARE_CREATION"

        # Department H: Control & Governance
        if any(w in cleaned for w in ["security", "threat", "iam", "governance", "audit", "observability", "quota"]):
            departments.add(DepartmentEnum.DEPT_H)
            capabilities.update([41, 42, 43, 45])
            intent = "SECURITY_AND_GOVERNANCE"

        # Department I: Advanced Intelligence
        if any(w in cleaned for w in ["patent", "theorem", "gap", "future scenario", "scenario", "dpll"]):
            departments.add(DepartmentEnum.DEPT_I)
            capabilities.update([46, 47, 48, 49])
            intent = "ADVANCED_DISCOVERY"

        # Fallback to Universal Intelligence if nothing detected
        if not departments:
            departments.add(DepartmentEnum.DEPT_A)
            capabilities.add(1)

        return ProjectDirective(
            directive_id=directive_id,
            raw_input=raw_input,
            user_id=user_id,
            intent=intent,
            target_departments=list(departments),
            requested_capabilities=sorted(list(capabilities)),
            priority=priority,
            timestamp_hlc=self._next_hlc(),
        )

    def list_capabilities(self) -> List[CapabilityDescriptor]:
        return self.registry.get_all()

    def get_capability(self, cap_id: int) -> Optional[CapabilityDescriptor]:
        return self.registry.get_by_id(cap_id)
