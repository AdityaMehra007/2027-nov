import subprocess
import sys

def test_cli_directive_summary():
    res = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "directive", "--summary"],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    assert res.returncode == 0
    assert "CASHFLOW INFINITY: OMNIVERSE & AETHER RESILIENCE FABRIC" in res.stdout
    assert "12 Planetary Services" in res.stdout
    assert "7 Executive Agent Roles Active" in res.stdout

def test_cli_directive_json():
    res = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "directive", "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    assert res.returncode == 0
    assert '"valid": true' in res.stdout.lower() or '"valid":true' in res.stdout.lower()
