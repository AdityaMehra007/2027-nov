# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Test suite for Phase 6 & 7 Agent Workforce & Orchestration Governor (PROJECT ONE)."""

import pytest
from omniverse.modules.opportunities.workforce import (
    WorkforceOrchestrator,
    AgentRole,
    TaskPriority,
    WorkforceTask,
    MerkleAuditBlock,
)


def test_workforce_role_registry():
    """Verify that all 6 canonical workforce roles are configured with bounded authority."""
    orchestrator = WorkforceOrchestrator()
    roles = orchestrator.list_roles()

    assert len(roles) == 6
    role_names = {r.role for r in roles}
    assert AgentRole.MARKET_RESEARCHER in role_names
    assert AgentRole.PROSPECTOR in role_names
    assert AgentRole.DELIVERY_ENGINEER in role_names
    assert AgentRole.QA_INSPECTOR in role_names
    assert AgentRole.FINANCIAL_CONTROLLER in role_names
    assert AgentRole.SECURITY_OFFICER in role_names

    for r in roles:
        assert r.token_budget_per_task > 0
        assert r.max_execution_timeout_sec > 0
        assert len(r.authority_boundaries) > 0


def test_dispatch_task_and_merkle_audit():
    """Verify task dispatch under token budget and Merkle audit block chaining."""
    orchestrator = WorkforceOrchestrator()

    task = orchestrator.dispatch_task(
        role=AgentRole.DELIVERY_ENGINEER,
        action="GENERATE_WORKFLOW_AUDIT",
        parameters={"client_name": "London Thames Logistics", "volume": 2800},
        priority=TaskPriority.HIGH,
    )

    assert isinstance(task, WorkforceTask)
    assert task.status == "COMPLETED"
    assert task.tokens_used <= 5000
    assert task.merkle_block_hash is not None

    # Check Merkle audit ledger
    ledger = orchestrator.get_merkle_ledger()
    assert len(ledger) >= 1
    latest_block = ledger[-1]
    assert latest_block.action == "GENERATE_WORKFLOW_AUDIT"
    assert len(latest_block.block_hash) == 64  # SHA-256


def test_gated_action_governance():
    """Verify that high-impact capital actions (> $10k) require human cryptographic approval."""
    orchestrator = WorkforceOrchestrator()

    gated_task = orchestrator.dispatch_task(
        role=AgentRole.FINANCIAL_CONTROLLER,
        action="TRANSFER_TREASURY_FUNDS",
        parameters={"amount_usd": 25000.0, "destination": "EXTERNAL_VENDOR"},
    )

    assert gated_task.status == "GATED_PENDING_APPROVAL"
    assert gated_task.is_gated is True
    assert orchestrator.has_pending_approvals() is True

    # Standup summary includes the gated count
    standup = orchestrator.generate_daily_standup()
    assert standup["pending_approvals_count"] >= 1
    assert "FINANCIAL_CONTROLLER" in standup["role_breakdown"]
