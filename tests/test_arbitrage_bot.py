# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Tests for Autonomous Arbitrage Bot."""

import pytest
from omniverse.modules.finance.arbitrage_bot import AutonomousArbitrageBot, ArbitrageTradeRecord


def test_arbitrage_bot_initialization():
    bot = AutonomousArbitrageBot()
    assert bot is not None
    assert len(bot.TRIANGLES) >= 4
    status = bot.get_bot_status()
    assert status["status"] == "ACTIVE_MONITORING"
    assert status["cumulative_profit_inr"] == 0.0


def test_arbitrage_bot_scan_and_execute():
    bot = AutonomousArbitrageBot()
    scans = bot.scan_all_triangles(capital=100_000.0)
    assert len(scans) == len(bot.TRIANGLES)

    cycle_result = bot.execute_arbitrage_cycle(capital=100_000.0)
    assert cycle_result["status"] == "COMPLETED"
    assert cycle_result["scanned_triangles"] == len(bot.TRIANGLES)
    assert "cumulative_treasury_profit_inr" in cycle_result
