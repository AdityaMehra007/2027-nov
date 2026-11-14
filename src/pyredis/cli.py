"""CLI entrypoint for PyRedis server."""

from __future__ import annotations
import argparse
import asyncio
import logging
import signal
import sys
from pyredis.server import RedisServer


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pyredis",
        description="PyRedis - High-Performance Zero-Dependency Redis Clone in Python",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address to bind (default: 127.0.0.1)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=6379,
        help="Port to listen on (default: 6379)",
    )
    parser.add_argument(
        "--aof-file",
        default="appendonly.aof",
        help="Path to Append-Only File for persistence (default: appendonly.aof, set empty to disable)",
    )
    return parser.parse_args(args)


async def main_async() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    aof_path = args.aof_file if args.aof_file else None
    server = RedisServer(host=args.host, port=args.port, aof_filepath=aof_path)

    await server.start()
    print(f"[*] PyRedis is ready to accept connections on {args.host}:{server.actual_port}")
    if aof_path:
        print(f"[*] AOF Persistence active: {aof_path}")

    stop_event = asyncio.Event()

    def handle_stop(*_):
        print("\n[*] Shutting down PyRedis...")
        stop_event.set()

    loop = asyncio.get_running_loop()
    if sys.platform != "win32":
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, handle_stop)
    else:
        # On Windows, signal handler support in asyncio is limited
        pass

    try:
        await stop_event.wait()
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        await server.stop()
        print("[*] PyRedis shutdown complete.")


def main() -> None:
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
