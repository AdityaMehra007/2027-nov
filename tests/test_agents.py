import pytest
from omniverse.agents.base import AgentDispatcher, AgentTask
from omniverse.agents.executive import ChiefRevenueArchitect
from omniverse.agents.commercial import SalesDirector
from omniverse.agents.quant import QuantAnalyst

def test_chief_revenue_architect_evaluation():
    agent = ChiefRevenueArchitect()
    task = AgentTask(
        task_type="evaluate_opportunity",
        payload={
            "niche": "Specialty Coffee Roaster",
            "city": "Bengaluru",
            "market_size_est": "Medium",
            "urgency": "High"
        }
    )
    result = agent.execute_task(task)
    
    assert result["agent"] == "ChiefRevenueArchitect"
    assert "strategic_recommendation" in result
    assert result["priority_level"] in ("HIGH", "MEDIUM", "LOW")

def test_sales_director_proposal_strategy():
    agent = SalesDirector()
    task = AgentTask(
        task_type="prepare_pitch",
        payload={
            "business_name": "Artisan Bakery",
            "estimated_value_inr": 25000.0
        }
    )
    result = agent.execute_task(task)
    
    assert result["agent"] == "SalesDirector"
    assert "pitch_strategy" in result
    assert "closing_cta" in result

def test_quant_analyst_risk_review():
    agent = QuantAnalyst()
    task = AgentTask(
        task_type="risk_assessment",
        payload={
            "strategy": "Momentum Breakout",
            "max_drawdown_pct": 12.5,
            "sharpe_ratio": 1.85
        }
    )
    result = agent.execute_task(task)
    
    assert result["agent"] == "QuantAnalyst"
    assert result["risk_verdict"] == "APPROVED"

def test_agent_dispatcher():
    dispatcher = AgentDispatcher()
    dispatcher.register(ChiefRevenueArchitect())
    dispatcher.register(SalesDirector())
    dispatcher.register(QuantAnalyst())
    
    task = AgentTask(
        task_type="evaluate_opportunity",
        payload={"niche": "Tech Consulting", "city": "Bengaluru"}
    )
    result = dispatcher.dispatch("ChiefRevenueArchitect", task)
    assert result["agent"] == "ChiefRevenueArchitect"
