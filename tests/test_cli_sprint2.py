# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

import sys
import subprocess
import pytest


def test_cli_agency_outreach():
    res = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "agency-outreach", "--channel", "ALL", "--limit", "2"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "OMNIVERSE MULTI-CHANNEL AGENCY OUTREACH" in res.stdout
    assert "Total Dispatched" in res.stdout
    assert "Success Rate" in res.stdout


def test_cli_saas_fleet_summary():
    res = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "saas-fleet", "--action", "summary"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "OMNIVERSE VERTICAL SAAS HOLDINGS FLEET" in res.stdout
    assert "Total Tenants" in res.stdout
    assert "Combined MRR" in res.stdout
    assert "CLOUDBITE" in res.stdout


def test_cli_saas_fleet_provision():
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "omniverse.cli",
            "saas-fleet",
            "--action",
            "provision",
            "--name",
            "AeroFit Pro Center",
            "--vertical",
            "GymVerse",
            "--plan",
            "enterprise",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "TENANT PROVISIONED: AeroFit Pro Center" in res.stdout
    assert "GYMVERSE" in res.stdout
    assert "ENTERPRISE" in res.stdout


def test_cli_clearing_settle():
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "omniverse.cli",
            "clearing-settle",
            "--amount",
            "25000",
            "--source-cur",
            "USD",
            "--target-cur",
            "INR",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "OMNISWARM ATOMIC TREASURY CLEARING SETTLEMENT" in res.stdout
    assert "TX-RTGS-" in res.stdout
    assert "SETTLED" in res.stdout
    assert "Fee Captured" in res.stdout
