"""Omniverse Global Opportunity & Career Intelligence Subsystem (PROJECT ONE)."""

from omniverse.modules.opportunities.models import (
    OpportunityType,
    StartupDeal,
    CareerMatch,
    TenderViability,
)
from omniverse.modules.opportunities.engine import GlobalOpportunityEngine
from omniverse.modules.opportunities.taxonomy import (
    CustomerTaxonomy,
    CustomerCategory,
    RevenueModelCatalogue,
    RevenueModel,
)
from omniverse.modules.opportunities.scoring import (
    OpportunityScorer,
    ScoredOpportunity,
)
from omniverse.modules.opportunities.company_intelligence import (
    CompanyIntelligenceRegistry,
    CompanyRecord,
    RegistrySource,
)
from omniverse.modules.opportunities.beachhead import (
    BeachheadAuditGenerator,
    AuditDeliverable,
)

__all__ = [
    "OpportunityType",
    "StartupDeal",
    "CareerMatch",
    "TenderViability",
    "GlobalOpportunityEngine",
    "CustomerTaxonomy",
    "CustomerCategory",
    "RevenueModelCatalogue",
    "RevenueModel",
    "OpportunityScorer",
    "ScoredOpportunity",
    "CompanyIntelligenceRegistry",
    "CompanyRecord",
    "RegistrySource",
    "BeachheadAuditGenerator",
    "AuditDeliverable",
]
