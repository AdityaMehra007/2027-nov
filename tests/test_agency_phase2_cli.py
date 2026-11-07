import subprocess
import sys
import pytest


def test_cli_agency_upi():
    result = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "agency-upi", "--order-id", "CLI_TEST_UPI", "--amount-usd", "75.0"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "CLI_TEST_UPI" in result.stdout
    assert "upi://" in result.stdout
    assert "Rs 6,450.00" in result.stdout


def test_cli_agency_crypto():
    result = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "agency-crypto", "--order-id", "CLI_TEST_CRYPTO", "--amount-usd", "250.0", "--chain", "BASE"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "CLI_TEST_CRYPTO" in result.stdout
    assert "BASE" in result.stdout
    assert "0x742d35Cc6634C0532925a3b844Bc454e4438f44e" in result.stdout


def test_cli_agency_pseo():
    result = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "agency-pseo", "--competitor", "Asana", "--our-solution", "Omniverse Ops Swarm", "--service", "AGENT_AUTOMATION"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "asana-alternative" in result.stdout
    assert "Omniverse Ops Swarm" in result.stdout


def test_cli_agency_daemon():
    result = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "agency-daemon", "--limit", "1", "--budget", "1500.0"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "DAEMON CYCLE" in result.stdout
    assert "Leads Hunted" in result.stdout


def test_cli_agency_revise():
    result = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "agency-revise", "--order-id", "CLI_REV_ORDER", "--feedback", "Include money-back guarantee in sales copy"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "REVISION AGENT" in result.stdout
    assert "QA Verified" in result.stdout
