import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from scripts import opendots_bridge

def test_get_status_running():
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "spaces": [{"id": "sp-1", "name": "Omniverse Space"}],
        "dots": [{"id": "dt-1", "name": "Atlas Dot", "instructions": "Coordinate global tasks."}],
        "setup": {"model": True, "browser": True, "intelligence": True}
    }).encode("utf-8")
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        status = opendots_bridge.get_status()
        assert status["running"] is True
        assert status["url"] == opendots_bridge.SERVER_URL
        assert len(status["spaces"]) == 1
        assert len(status["dots"]) == 1
        assert status["spaces"][0]["name"] == "Omniverse Space"
        assert status["setup"]["model"] is True

def test_get_status_offline():
    with patch("urllib.request.urlopen", side_effect=Exception("Connection refused")):
        status = opendots_bridge.get_status()
        assert status["running"] is False
        assert "Connection refused" in status["error"]

def test_start_server_already_running(capsys):
    with patch.object(opendots_bridge, "get_status", return_value={"running": True}):
        res = opendots_bridge.start_server(dev_mode=False)
        assert res is True
        captured = capsys.readouterr().out
        assert "already running" in captured

def test_start_server_launches_process(capsys):
    with patch.object(opendots_bridge, "get_status", return_value={"running": False}):
        mock_proc = MagicMock()
        mock_proc.pid = 9999
        with patch("subprocess.Popen", return_value=mock_proc) as mock_popen:
            res = opendots_bridge.start_server(dev_mode=True)
            assert res is True
            assert mock_popen.called
            captured = capsys.readouterr().out
            assert "Started process (PID 9999)" in captured

def test_print_summary(capsys):
    mock_status_online = {
        "running": True,
        "url": "http://127.0.0.1:4310",
        "spaces": [{"id": "s1", "name": "General Space"}],
        "dots": [{"id": "d1", "name": "Strategist", "instructions": "Direct operations across departments."}],
        "setup": {"model": True, "browser": False, "intelligence": True}
    }
    with patch.object(opendots_bridge, "get_status", return_value=mock_status_online):
        opendots_bridge.print_summary()
        out = capsys.readouterr().out
        assert "ONLINE [Active]" in out
        assert "General Space" in out
        assert "Strategist" in out

def test_print_summary_offline(capsys):
    mock_status_offline = {
        "running": False,
        "url": "http://127.0.0.1:4310",
        "error": "Server unreachable"
    }
    with patch.object(opendots_bridge, "get_status", return_value=mock_status_offline):
        opendots_bridge.print_summary()
        out = capsys.readouterr().out
        assert "OFFLINE" in out
        assert "Server unreachable" in out

def test_main_cli_dispatch():
    with patch.object(opendots_bridge, "print_summary") as mock_summary:
        with patch.object(sys, "argv", ["opendots_bridge.py", "--status"]):
            opendots_bridge.main()
            assert mock_summary.called

    with patch.object(opendots_bridge, "start_server") as mock_start:
        with patch.object(sys, "argv", ["opendots_bridge.py", "--start", "--dev"]):
            opendots_bridge.main()
            mock_start.assert_called_once_with(dev_mode=True)
