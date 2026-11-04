"""Omniverse Central Agent Workforce Hierarchy."""

from omniverse.agents.base import BaseAgent, AgentTask, AgentDispatcher
from omniverse.agents.executive import ChiefRevenueArchitect
from omniverse.agents.commercial import SalesDirector
from omniverse.agents.quant import QuantAnalyst
from omniverse.agents.deep_tech import DeepTechArchitect
from omniverse.agents.governance import GovernanceOfficer

from omniverse.agents.global_prospector import GlobalProspectorAgent
from omniverse.agents.client_diagnostic import ClientDiagnosticAgent
from omniverse.agents.solution_architect import UniversalSolutionArchitectAgent
from omniverse.agents.code_forge_agent import AutonomousCodeForgeAgent
from omniverse.agents.agent_engineer_agent import AutonomousAgentEngineerAgent
from omniverse.agents.growth_marketing_agent import GrowthMarketingAgent
from omniverse.agents.commercial_closer import CommercialDealCloserAgent
from omniverse.agents.treasury_reconciler import TreasuryReconciliationAgent
from omniverse.agents.swarm_orchestrator import SupremeSwarmOrchestrator

__all__ = [
    "BaseAgent",
    "AgentTask",
    "AgentDispatcher",
    "ChiefRevenueArchitect",
    "SalesDirector",
    "QuantAnalyst",
    "DeepTechArchitect",
    "GovernanceOfficer",
    "GlobalProspectorAgent",
    "ClientDiagnosticAgent",
    "UniversalSolutionArchitectAgent",
    "AutonomousCodeForgeAgent",
    "AutonomousAgentEngineerAgent",
    "GrowthMarketingAgent",
    "CommercialDealCloserAgent",
    "TreasuryReconciliationAgent",
    "SupremeSwarmOrchestrator",
]
