import sys
import subprocess
import pytest


def test_cli_agency_hunt():
    res = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "agency-hunt", "--limit", "2"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "AUTONOMOUS LEAD ACQUISITION" in res.stdout
    assert "Discovered" in res.stdout


def test_cli_agency_audit():
    res = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "agency-audit", "--lead-name", "Quantum BioLabs", "--revenue", "400000"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "DIAGNOSTIC GAP ANALYSIS" in res.stdout
    assert "Estimated Monthly Loss" in res.stdout


def test_cli_agency_pitch():
    res = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "agency-pitch", "--lead-name", "Stellar Goods", "--archetype", "ECOMMERCE"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "CONVERSION PITCH & OUTREACH CTA" in res.stdout
    assert "https://wa.me/" in res.stdout


def test_cli_agency_fulfill(tmp_path):
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "omniverse.cli",
            "agency-fulfill",
            "--client",
            "Alpha Corp",
            "--service",
            "FULLSTACK_DEV",
            "--brief",
            "Landing page with API",
            "--budget",
            "3000",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "AUTONOMOUS FULFILLMENT & QA GATING" in res.stdout
    assert "QA Status: PASSED" in res.stdout


def test_cli_agency_status():
    res = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "agency-status"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    assert "AUTONOMOUS AGENCY OPERATING MATRIX" in res.stdout
    assert "Pipeline Value" in res.stdout
