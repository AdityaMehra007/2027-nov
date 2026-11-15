"""Tests for PyGit CLI entry point."""

import subprocess
import sys
import tempfile
import os


def test_pygit_cli_help():
    cli_py = os.path.abspath("src/pygit/cli.py")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath("src")
    res = subprocess.run([sys.executable, cli_py, "--help"], capture_output=True, text=True, env=env)
    assert res.returncode == 0
    assert "Zero-dependency Git implementation in Python" in res.stdout


def test_pygit_cli_workflow():
    cli_py = os.path.abspath("src/pygit/cli.py")
    with tempfile.TemporaryDirectory() as tmpdir:
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.abspath("src")

        # 1. pygit init
        res = subprocess.run([sys.executable, cli_py, "init", tmpdir], capture_output=True, text=True, env=env)
        assert res.returncode == 0
        assert "Initialized empty Git repository" in res.stdout

        # 2. create file
        f = os.path.join(tmpdir, "test.txt")
        with open(f, "w", encoding="utf-8", newline="\n") as fp:
            fp.write("Hello CLI\n")

        # 3. hash-object
        res = subprocess.run([sys.executable, cli_py, "hash-object", f], capture_output=True, text=True, cwd=tmpdir, env=env)
        assert res.returncode == 0
        assert len(res.stdout.strip()) == 40
