import pytest
from omniverse.core.llm_arbitrator import (
    HybridLLMArbitrator,
    ModelProvider,
    ModelTier,
    TaskCategory,
    ArbitrationRequest,
    ModelSpec
)
from omniverse.core.telemetry import global_event_bus

def test_llm_arbitrator_registry():
    arbitrator = HybridLLMArbitrator()
    assert "gemini-1.5-pro" in arbitrator.registry
    assert "claude-3-5-sonnet" in arbitrator.registry
    assert "gpt-4o" in arbitrator.registry
    assert "qwen-2.5-coder-32b" in arbitrator.registry
    assert "llama-3.1-70b-vllm" in arbitrator.registry

    model = arbitrator.get_model("gemini-1.5-pro")
    assert model is not None
    assert model.provider == ModelProvider.GEMINI
    assert model.tier == ModelTier.FRONTIER
    assert model.offline_capable is False

def test_cost_estimation():
    arbitrator = HybridLLMArbitrator()
    # Offline model has zero marginal token cost
    offline_cost = arbitrator.estimate_cost(1000, 500, "qwen-2.5-coder-32b")
    assert offline_cost == 0.0

    # Frontier model cost
    gemini_cost = arbitrator.estimate_cost(1000, 1000, "gemini-1.5-pro")
    assert gemini_cost > 0.0
    assert gemini_cost == round(0.00125 + 0.0050, 6)

def test_route_strategic_reasoning():
    arbitrator = HybridLLMArbitrator()
    req = ArbitrationRequest(
        prompt="Design a 10-year federated resilience thesis for sovereign edge clusters.",
        task_category=TaskCategory.STRATEGIC_REASONING
    )
    result = arbitrator.route(req)
    assert result.selected_model.tier == ModelTier.FRONTIER or result.selected_model.offline_capable
    assert len(result.fallback_chain) >= 3

def test_route_offline_sovereign_constraint():
    arbitrator = HybridLLMArbitrator()
    req = ArbitrationRequest(
        prompt="Air-gapped classified ledger reconciliation.",
        task_category=TaskCategory.OFFLINE_SOVEREIGN,
        requires_offline=True
    )
    result = arbitrator.route(req)
    assert result.selected_model.offline_capable is True
    assert result.primary_provider in (ModelProvider.OLLAMA, ModelProvider.VLLM)
    # Check that fallback chain only contains offline-capable models
    for m_id in result.fallback_chain:
        assert arbitrator.registry[m_id].offline_capable is True

def test_route_preferred_provider():
    arbitrator = HybridLLMArbitrator()
    req = ArbitrationRequest(
        prompt="Explain distributed consensus.",
        preferred_provider=ModelProvider.OPENAI
    )
    result = arbitrator.route(req)
    assert result.primary_provider == ModelProvider.OPENAI
    assert result.selected_model.model_id == "gpt-4o"

def test_route_low_latency_constraint():
    arbitrator = HybridLLMArbitrator()
    req = ArbitrationRequest(
        prompt="Rapid edge telemetry classification alert",
        task_category=TaskCategory.EDGE_CLASSIFICATION,
        max_latency_ms=50.0
    )
    result = arbitrator.route(req)
    assert result.selected_model.avg_latency_ms <= 50.0

def test_execute_with_automatic_failover():
    arbitrator = HybridLLMArbitrator()
    req = ArbitrationRequest(
        prompt="Compile high-throughput derivatives hedging strategy.",
        task_category=TaskCategory.CODE_GENERATION
    )
    initial_route = arbitrator.route(req)
    primary_provider = initial_route.primary_provider

    # Simulate upstream outage on the primary provider
    response = arbitrator.execute(req, mock_provider_failures=[primary_provider])

    assert response.success is True
    assert response.failover_occurred is True
    assert response.provider_used != primary_provider
    assert len(response.attempted_models) >= 2
    assert response.content is not None

def test_execute_telemetry_events():
    arbitrator = HybridLLMArbitrator()
    req = ArbitrationRequest(
        prompt="Quick general classification prompt",
        task_category=TaskCategory.GENERAL
    )
    response = arbitrator.execute(req)
    assert response.success is True
    assert response.tokens_used > 0
    assert response.actual_latency_ms > 0

    events = global_event_bus.get_events()
    event_names = [e["event_name"] for e in events]
    assert "LLM_ROUTED" in event_names
    assert "LLM_COMPLETED" in event_names

def test_empty_registry_raises_value_error():
    arbitrator = HybridLLMArbitrator(registry={})
    with pytest.raises(ValueError, match="Arbitrator registry cannot be empty"):
        arbitrator.route(ArbitrationRequest(prompt="test"))

def test_negative_tokens_clamped_to_zero():
    arbitrator = HybridLLMArbitrator()
    cost = arbitrator.estimate_cost(-500, -200, "gemini-1.5-pro")
    assert cost == 0.0

def test_strict_budget_online_only_fallback():
    # Registry with only commercial model
    arbitrator = HybridLLMArbitrator(registry={
        "gpt-4o": HybridLLMArbitrator.DEFAULT_REGISTRY["gpt-4o"]
    })
    req = ArbitrationRequest(prompt="Budget test", max_cost_usd=0.00000001)
    result = arbitrator.route(req)
    assert result.selected_model.model_id == "gpt-4o"

def test_all_providers_outage_heuristic_fallback():
    arbitrator = HybridLLMArbitrator()
    req = ArbitrationRequest(prompt="Simulate total infrastructure loss")
    # All providers offline
    all_providers = [
        ModelProvider.GEMINI,
        ModelProvider.ANTHROPIC,
        ModelProvider.OPENAI,
        ModelProvider.OLLAMA,
        ModelProvider.VLLM
    ]
    response = arbitrator.execute(req, mock_provider_failures=all_providers)
    assert response.success is True
    assert response.failover_occurred is True
    assert response.provider_used == ModelProvider.HEURISTIC_FALLBACK
    assert response.model_used == "rule-based-kernel-fallback"

