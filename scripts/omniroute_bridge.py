#!/usr/bin/env python3
"""
OmniRoute <-> OmniVerse Master Bridge
Controls, monitors, and routes inference through the OmniRoute AI Gateway inside CASHFLOW INFINITY: OMNIVERSE.
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.pycontrolplane.ai_gateway.omniroute_engine import OmniRouteEngine, CompressionMode
from src.pycontrolplane.ai_gateway.gateway_server import OmniRouteGatewayServer
from src.pycontrolplane.ai_gateway.compressor import PromptCompressor

GATEWAY_URL = os.environ.get("OMNIROUTE_URL", "http://127.0.0.1:4000")


def get_status() -> dict:
    """Checks online status of OmniRoute Gateway."""
    try:
        req = urllib.request.Request(f"{GATEWAY_URL}/health")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            data["running"] = True
            data["url"] = GATEWAY_URL
            return data
    except Exception as e:
        return {
            "running": False,
            "url": GATEWAY_URL,
            "error": str(e),
        }


def print_status() -> None:
    """Prints a human-readable telemetry summary of the OmniRoute Gateway."""
    status = get_status()
    print("=" * 65)
    print("   OMNIROUTE AI GATEWAY - OMNIVERSE RUNTIME STATUS")
    print("=" * 65)
    if status["running"]:
        print(f" Status:             ONLINE [Active]")
        print(f" URL:                {status['url']}")
        print(f" Service:            {status.get('service', 'OmniRoute')}")
        print(f" Version:            {status.get('version', '1.0.0')}")
        print(f" Requests Served:    {status.get('total_requests', 0)}")
        print(f" Tokens Saved:       {status.get('total_tokens_saved', 0)}")
        print(f" Configured Endpoints:{status.get('endpoints_count', 0)}")
        print(f" Cooldown Endpoints: {status.get('cooldown_endpoints', 0)}")
    else:
        print(f" Status:             OFFLINE (Native fallback available)")
        print(f" URL:                {status['url']}")
        print(f" Detail:             {status.get('error')}")

        # Show embedded engine status
        engine = OmniRouteEngine()
        print("\n [Embedded Native Engine Diagnostic]")
        print(f" Available Models:   {len(engine.endpoints)}")
        for name, ep in engine.endpoints.items():
            cost_str = "FREE" if ep.is_free else f"${ep.cost_per_million_input}/M in, ${ep.cost_per_million_output}/M out"
            print(f"   * {name:<22} [{ep.tier.value:<9}] -> {cost_str}")
    print("=" * 65)


def run_compression_demo(text: str, mode: str = "CAVEMAN") -> None:
    """Demonstrates prompt compression and token reduction."""
    compressor = PromptCompressor()
    c_mode = getattr(CompressionMode, mode.upper(), CompressionMode.CAVEMAN)
    compressed, stats = compressor.compress_text(text, mode=c_mode)

    print("=" * 65)
    print("   OMNIROUTE TOKEN COMPRESSOR (RTK + CAVEMAN)")
    print("=" * 65)
    print(f" Mode:               {stats.mode.value}")
    print(f" Original Chars:     {stats.original_chars}")
    print(f" Compressed Chars:   {stats.compressed_chars}")
    print(f" Est. Orig Tokens:   {stats.original_tokens_est}")
    print(f" Est. Comp Tokens:   {stats.compressed_tokens_est}")
    print(f" Reduction Ratio:    {stats.reduction_ratio * 100:.1f}%")
    print("-" * 65)
    print("[ORIGINAL]:")
    print(text)
    print("-" * 65)
    print("[COMPRESSED]:")
    print(compressed)
    print("=" * 65)


def start_native_server(port: int = 4000, blocking: bool = True) -> None:
    """Starts the native zero-dependency Python OmniRoute HTTP server."""
    server = OmniRouteGatewayServer(host="127.0.0.1", port=port)
    server.start(blocking=blocking)


def main():
    parser = argparse.ArgumentParser(description="OmniRoute AI Gateway Master Bridge")
    parser.add_argument("--status", action="store_true", help="Inspect gateway health and metrics")
    parser.add_argument("--start", action="store_true", help="Start native Python OmniRoute gateway server")
    parser.add_argument("--port", type=int, default=4000, help="Gateway port (default: 4000)")
    parser.add_argument("--compress", type=str, help="Run prompt compression on supplied text")
    parser.add_argument("--mode", type=str, default="CAVEMAN", choices=["PASSTHROUGH", "LIGHT", "CAVEMAN", "AGGRESSIVE"])
    args = parser.parse_args()

    if args.compress:
        run_compression_demo(args.compress, mode=args.mode)
    elif args.start:
        start_native_server(port=args.port, blocking=True)
    else:
        print_status()


if __name__ == "__main__":
    main()
