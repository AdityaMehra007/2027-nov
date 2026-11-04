import pytest
from unittest.mock import patch
import sys
from omniverse.cli import main


def test_cli_conglomerate_command(capsys):
    test_args = ["omniverse", "conglomerate", "--cycles", "1", "--briefing"]
    with patch.object(sys, "argv", test_args):
        main()

    captured = capsys.readouterr().out
    assert "AUTONOMOUS CONGLOMERATE" in captured
    assert "Cycle" in captured
    assert "Pipeline Value" in captured


def test_cli_approvals_list_command(capsys):
    test_args = ["omniverse", "approvals", "--list"]
    with patch.object(sys, "argv", test_args):
        main()

    captured = capsys.readouterr().out
    assert "AIR-GAPPED APPROVALS" in captured


def test_cli_simulate_webhook_stripe(capsys):
    test_args = ["omniverse", "simulate-webhook", "--gateway", "stripe", "--amount", "250.0"]
    with patch.object(sys, "argv", test_args):
        main()

    captured = capsys.readouterr().out
    assert "PAYMENT WEBHOOK SIMULATION" in captured
    assert "Stripe" in captured
