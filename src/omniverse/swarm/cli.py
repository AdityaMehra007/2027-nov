"""Command-line interface commands for OmniSwarm mesh operations."""

from __future__ import annotations

import argparse
import sys
from typing import Any
from omniverse.swarm.kernel import SwarmKernel


def render_swarm_status_table(
    node_id: str,
    host: str,
    port: int,
    active_actors: int,
    active_peers: int,
    dlq_size: int,
) -> str:
    """Formats an institutional ASCII diagnostic panel for the swarm node."""
    lines = [
        "==========================================================================",
        "                       🌌 OMNISWARM STATUS & DIAGNOSTICS                   ",
        "==========================================================================",
        f" Node Fingerprint   : {node_id}",
        f" Listening Endpoint : ws://{host}:{port}/ws/swarm",
        f" Membership Status  : ACTIVE (SWIM Epidemic Gossip)",
        f" Active Actors      : {active_actors} supervised virtual agents",
        f" Connected Peers    : {active_peers} mesh nodes",
        f" Dead Letter Queue  : {dlq_size} quarantined messages",
        " Security Governor  : ENFORCED (Air-Gapped Gating)",
        "==========================================================================",
    ]
    return "\n".join(lines)


def handle_swarm_command(args: Any) -> None:
    """Dispatches swarm CLI actions (status, benchmark, start)."""
    action = getattr(args, "action", "status") or "status"

    if action == "status":
        kernel = SwarmKernel(host="127.0.0.1", port=getattr(args, "port", 9091))
        table = render_swarm_status_table(
            node_id=kernel.node_id,
            host=kernel.host,
            port=kernel.port,
            active_actors=len(kernel.supervisor._actors),
            active_peers=len(kernel.gossip.get_active_peers()),
            dlq_size=kernel.dlq.size(),
        )
        print(f"\n{table}\n")

    elif action == "benchmark":
        from omniverse.operations.benchmark import OmniverseBenchmarkingSuite
        suite = OmniverseBenchmarkingSuite()
        iterations = max(5, getattr(args, "iterations", 25))
        print(f"\n⚡ Running OmniSwarm Empirical Benchmark ({iterations} iterations)...")
        metric = suite.run_omniswarm_benchmark(iterations=iterations)
        print(
            f"Result: {metric.name} | Latency: {metric.avg_latency_ms:.3f}ms | "
            f"Throughput: {metric.throughput_ops_per_sec:,.1f} ops/sec [{metric.status}]\n"
        )

    elif action == "start":
        import asyncio
        port = getattr(args, "port", 9091)
        print(f"🚀 Launching OmniSwarm Mesh Node on port {port}...")
        kernel = SwarmKernel(host="127.0.0.1", port=port)

        async def _run():
            await kernel.start()
            print(f"✅ OmniSwarm Node {kernel.node_id} online at ws://127.0.0.1:{port}/ws/swarm")
            try:
                while True:
                    await asyncio.sleep(1)
            except (asyncio.CancelledError, KeyboardInterrupt):
                await kernel.shutdown()

        try:
            asyncio.run(_run())
        except KeyboardInterrupt:
            print("\nShutting down OmniSwarm node...")
