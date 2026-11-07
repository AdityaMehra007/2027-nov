# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

import sys
import subprocess
import pytest


def test_cli_arbitrage_bot():
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "omniverse.cli",
            "arbitrage-bot",
            "--capital",
            "50000",
            "--min-profit",
            "0.0",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "OMNIVERSE AUTONOMOUS ARBITRAGE BOT EXECUTION" in res.stdout
    assert "Scanned Triangles" in res.stdout
    assert "Treasury Profit" in res.stdout


def test_cli_agency_cycle():
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "omniverse.cli",
            "agency-cycle",
            "--limit",
            "1",
            "--budget",
            "2000",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "OMNIVERSE AUTONOMOUS AGENCY CYCLE EXECUTION" in res.stdout
    assert "Leads Discovered" in res.stdout
    assert "Orders Created" in res.stdout
    assert "Pipeline Value" in res.stdout
