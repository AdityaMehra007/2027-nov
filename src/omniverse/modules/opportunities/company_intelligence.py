# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Company Intelligence Registry & Target Discovery (PROJECT ONE)."""

import enum
import time
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set


class RegistrySource(str, enum.Enum):
    PUBLIC_TECH_INDEX = "PUBLIC_TECH_INDEX"
    REGULATORY_FILING = "REGULATORY_FILING"
    ECOMMERCE_DIRECTORY = "ECOMMERCE_DIRECTORY"
    COMMERCIAL_REGISTRY = "COMMERCIAL_REGISTRY"
    MANUAL_RESEARCH = "MANUAL_RESEARCH"


@dataclass
class CompanyRecord:
    name: str
    website: str
    country: str
    city: str
    industry: str
    source: RegistrySource
    buying_signals: List[str] = field(default_factory=list)
    operational_pain_indicators: List[str] = field(default_factory=list)
    confidence_score: float = 0.8
    verified: bool = False
    id: str = field(default_factory=lambda: f"comp_{uuid.uuid4().hex[:12]}")
    created_at: float = field(default_factory=time.time)


class CompanyIntelligenceRegistry:
    """In-memory and persistent storage for target account profiles with deduplication."""

    def __init__(self):
        self._records: Dict[str, CompanyRecord] = {}
        self._seen_websites: Set[str] = set()
        self._seen_names: Set[str] = set()

    def _normalize_url(self, url: str) -> str:
        u = url.strip().lower()
        u = u.replace("https://", "").replace("http://", "").replace("www.", "")
        return u.rstrip("/")

    def register_company(self, record: CompanyRecord) -> bool:
        """Registers a company record with strict URL and corporate name deduplication."""
        norm_url = self._normalize_url(record.website)
        norm_name = record.name.strip().lower()

        if norm_url in self._seen_websites or norm_name in self._seen_names:
            return False

        self._records[record.id] = record
        if norm_url:
            self._seen_websites.add(norm_url)
        self._seen_names.add(norm_name)
        return True

    def count(self) -> int:
        return len(self._records)

    def get_company(self, company_id: str) -> Optional[CompanyRecord]:
        return self._records.get(company_id)

    def list_companies(self) -> List[CompanyRecord]:
        return list(self._records.values())
