import subprocess
import sys
import pytest

def test_cli_help():
    res = subprocess.run([sys.executable, "-m", "omniverse.cli", "--help"], capture_output=True, text=True, encoding="utf-8")
    assert res.returncode == 0
    assert "status" in res.stdout
    assert "tui" in res.stdout
    assert "benchmark" in res.stdout

def test_cli_tui_cycles():
    res = subprocess.run([sys.executable, "-m", "omniverse.cli", "tui", "--cycles", "1", "--no-ansi"], capture_output=True, text=True, encoding="utf-8")
    assert res.returncode == 0
    assert "OMNIVERSE" in res.stdout
    assert "PLANETARY EDGE NODES" in res.stdout

def test_cli_benchmark():
    res = subprocess.run([sys.executable, "-m", "omniverse.cli", "benchmark", "--iterations", "3"], capture_output=True, text=True, encoding="utf-8")
    assert res.returncode == 0
    assert "CASHFLOW INFINITY EMPIRICAL BENCHMARK" in res.stdout
    assert "PBFT" in res.stdout

def test_cli_pbft():
    res = subprocess.run([sys.executable, "-m", "omniverse.cli", "pbft-consensus", "--nodes", "4", "--adversaries", "1"], capture_output=True, text=True, encoding="utf-8")
    assert res.returncode == 0
    assert "PRACTICAL BYZANTINE FAULT TOLERANCE" in res.stdout

def test_cli_tui_piped_stdin():
    p = subprocess.Popen(
        [sys.executable, "-m", "omniverse.cli", "tui", "--no-ansi"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )
    stdout, _ = p.communicate(input="q\n", timeout=5)
    assert p.returncode == 0
    assert "OMNIVERSE" in stdout

def test_cli_benchmark_zero_iterations():
    res = subprocess.run(
        [sys.executable, "-m", "omniverse.cli", "benchmark", "--iterations", "0"],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    assert res.returncode == 0
    assert "CASHFLOW INFINITY EMPIRICAL BENCHMARK" in res.stdout

