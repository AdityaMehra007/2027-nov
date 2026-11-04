"""Omniverse Global Opportunity & Career Intelligence Subsystem."""

from omniverse.modules.opportunities.models import (
    OpportunityType,
    StartupDeal,
    CareerMatch,
    TenderViability
)
from omniverse.modules.opportunities.engine import GlobalOpportunityEngine

__all__ = [
    "OpportunityType",
    "StartupDeal",
    "CareerMatch",
    "TenderViability",
    "GlobalOpportunityEngine"
]
