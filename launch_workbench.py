#!/usr/bin/env python3
# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Standalone Launcher for BYOX Interactive Visual Workbench.

Integrates and showcases 6 canonical systems built entirely from scratch:
1. PyRedis (In-memory KV, RESP2 parser, TTL sweep, AOF persistence)
2. PyGit (Content-addressed store, Merkle tree, index, status, diff)
3. PyDB (Paged 4KB binary pager, B-tree engine, SQL lexer & parser)
4. PyShell (Tokenizer, pipeline chaining, redirection, builtins)
5. PyWeb (Async HTTP/1.1 streaming parser, RFC 6455 WebSocket engine)
6. PyTransformer (Scalar autograd, multi-head attention, tokenizer)

Zero external runtime dependencies. 100% Python 3.13 Standard Library.
"""

from __future__ import annotations
import argparse
import asyncio
import os
import signal
import sys
import webbrowser

from byox.workbench.server import WorkbenchServer

BANNER = r"""
  ____  __   __  _____  __  __   ____  _             _ _       
 | __ ) \ \ / / / _ \ \/ / / /_ / ___|| |_ _   _  __| (_) ___  
 |  _ \  \ V / | | | \  / | '_ \\___ \| __| | | |/ _` | |/ _ \ 
 | |_) |  | |  | |_| /  \ | (_) |___) | |_| |_| | (_| | | (_) |
 |____/   |_|   \___/_/\_\ \___/|____/ \__|\__,_|\__,_|_|\___/ 
 ===============================================================
   INTERACTIVE MULTI-ENGINE BENCHMARK & VISUAL WORKBENCH
       100% Built From Scratch | Zero Runtime Dependencies
 ===============================================================
"""


async def main() -> None:
    parser = argparse.ArgumentParser(description="BYOX Visual Workbench & Multi-Engine Studio")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9000, help="Port to listen on (default: 9000)")
    parser.add_argument("--db", default="data/workbench.db", help="Path to PyDB storage file (default: data/workbench.db)")
    parser.add_argument("--repo", default=".", help="Path to PyGit repository root (default: current directory)")
    parser.add_argument("--open-browser", action="store_true", help="Automatically open browser tab on startup")
    args = parser.parse_args()

    print(BANNER)
    server = WorkbenchServer(host=args.host, port=args.port, db_path=args.db, repo_path=args.repo)
    srv = await server.start()

    url = f"http://{args.host}:{server.actual_port}/"
    print(f"[*] BYOX Studio is live and listening at:")
    print(f"    -> Web UI & REST API: {url}")
    print(f"    -> PyShell WebSocket:  ws://{args.host}:{server.actual_port}/ws/shell")
    print(f"    -> PyTransformer WS:   ws://{args.host}:{server.actual_port}/ws/llm")
    print(f"[*] Active Engines:")
    print(f"    [+] PyRedis:       Operational (TTL sweeper active)")
    print(f"    [+] PyDB:          Operational (Paged 4KB pager connected)")
    print(f"    [+] PyGit:         Operational (VCS Merkle store connected)")
    print(f"    [+] PyShell:       Operational (Interactive pseudo-terminal)")
    print(f"    [+] PyWeb:         Operational (HTTP/1.1 + RFC 6455 WebSockets)")
    print(f"    [+] PyTransformer: Operational (Autograd attention engine)")
    print("\nPress Ctrl+C to terminate cleanly.\n")

    if args.open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    stop_event = asyncio.Event()

    def handle_sig(*_):
        stop_event.set()

    if sys.platform != "win32":
        loop = asyncio.get_running_loop()
        for s in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(s, handle_sig)

    try:
        if sys.platform == "win32":
            while not stop_event.is_set():
                await asyncio.sleep(0.5)
        else:
            await stop_event.wait()
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        print("\n[*] Shutting down BYOX Workbench...")
        await server.stop()
        print("[*] All engines closed cleanly.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
