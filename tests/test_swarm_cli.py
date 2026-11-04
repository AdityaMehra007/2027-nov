"""Tests for OmniSwarm CLI subcommands and benchmark suite integration."""

import pytest
from omniverse.operations.benchmark import OmniverseBenchmarkingSuite
from omniverse.swarm.cli import handle_swarm_command, render_swarm_status_table


def test_swarm_benchmark_metric_in_suite():
    suite = OmniverseBenchmarkingSuite()
    metric = suite.run_omniswarm_benchmark(iterations=25)

    assert metric.name == "OmniSwarm Ed25519 & Actor Dispatch"
    assert metric.status == "PASSED"
    assert metric.iterations == 25
    assert metric.throughput_ops_per_sec > 100.0
    assert metric.avg_latency_ms >= 0.0


def test_swarm_status_rendering():
    table = render_swarm_status_table(
        node_id="node_1122334455667788",
        host="127.0.0.1",
        port=9091,
        active_actors=5,
        active_peers=3,
        dlq_size=0,
    )
    assert "node_1122334455667788" in table
    assert "9091" in table
    assert "OMNISWARM STATUS" in table


def test_swarm_cli_handler_status(capsys):
    class Args:
        action = "status"
        port = 9091
        iterations = 10

    handle_swarm_command(Args())
    captured = capsys.readouterr()
    assert "OMNISWARM STATUS" in captured.out


def test_swarm_cli_handler_benchmark(capsys):
    class Args:
        action = "benchmark"
        port = 9091
        iterations = 10

    handle_swarm_command(Args())
    captured = capsys.readouterr()
    assert "OmniSwarm Ed25519 & Actor Dispatch" in captured.out
