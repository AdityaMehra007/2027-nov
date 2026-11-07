# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Test suite for CLI do-everything command."""

import subprocess
import sys


def test_cli_do_everything():
    result = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "do-everything"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "CASHFLOW INFINITY: SUPREME 'DO EVERYTHING' MASTER RUN" in result.stdout
    assert "Health Probes" in result.stdout
    assert "Agency Daemon" in result.stdout
    assert "SaaS Template Store" in result.stdout
    assert "GODMODE Career OS" in result.stdout
    assert "Apex Singularity" in result.stdout
    assert "ALL ENGINES EXECUTED & 100% OPERATIONAL" in result.stdout
