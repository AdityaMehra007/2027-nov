"""PyWeb Async HTTP/1.1 and RFC 6455 WebSocket Benchmark."""

from __future__ import annotations
import asyncio
import time
from typing import List
from pyweb.http import HTTPResponse
from pyweb.server import WebServer
from pyweb.websocket import build_websocket_frame, parse_websocket_frame
from byox.benchmarks.metrics import BenchmarkResult


async def benchmark_pyweb(num_requests: int = 1000, concurrency: int = 10) -> List[BenchmarkResult]:
    server = WebServer(host="127.0.0.1", port=0)

    @server.route("/bench/json", method="GET")
    async def handle_json(req):
        return HTTPResponse.json({"status": "ok", "ts": time.time()})

    @server.websocket("/bench/ws")
    async def handle_ws(reader, writer):
        while not reader.at_eof():
            data = await reader.read(4096)
            if not data:
                break
            frame = parse_websocket_frame(data)
            if frame:
                reply = build_websocket_frame(frame.payload, opcode=frame.opcode)
                writer.write(reply)
                await writer.drain()

    await server.start()
    port = server.actual_port
    results: List[BenchmarkResult] = []

    try:
        # 1. HTTP/1.1 Concurrent Request Benchmark
        http_latencies: List[float] = []
        reqs_per_worker = num_requests // concurrency

        async def http_worker():
            for _ in range(reqs_per_worker):
                r, w = await asyncio.open_connection("127.0.0.1", port)
                req_bytes = b"GET /bench/json HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"
                t0 = time.perf_counter()
                w.write(req_bytes)
                await w.drain()
                resp = await r.read(1024)
                http_latencies.append((time.perf_counter() - t0) * 1000.0)
                w.close()
                await w.wait_closed()

        t0_http = time.perf_counter()
        tasks = [http_worker() for _ in range(concurrency)]
        await asyncio.gather(*tasks)
        total_http_duration = time.perf_counter() - t0_http

        results.append(
            BenchmarkResult.from_latencies(
                name="PyWeb HTTP/1.1 JSON Request",
                latencies_ms=http_latencies,
                duration_sec=total_http_duration,
                metadata={"concurrency": concurrency, "total_requests": len(http_latencies)},
            )
        )

        # 2. WebSocket Roundtrip Ping-Pong Benchmark
        ws_latencies: List[float] = []
        r_ws, w_ws = await asyncio.open_connection("127.0.0.1", port)
        ws_handshake = (
            b"GET /bench/ws HTTP/1.1\r\n"
            b"Host: 127.0.0.1\r\n"
            b"Upgrade: websocket\r\n"
            b"Connection: Upgrade\r\n"
            b"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
            b"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        w_ws.write(ws_handshake)
        await w_ws.drain()
        await r_ws.read(1024)  # 101 Switching Protocols

        t0_ws = time.perf_counter()
        ws_frames_count = 200

        for i in range(ws_frames_count):
            msg = f"msg_{i}"
            frame = build_websocket_frame(msg, mask=True)
            t0 = time.perf_counter()
            w_ws.write(frame)
            await w_ws.drain()
            resp = await r_ws.read(1024)
            ws_latencies.append((time.perf_counter() - t0) * 1000.0)

        total_ws_duration = time.perf_counter() - t0_ws
        w_ws.close()
        await w_ws.wait_closed()

        results.append(
            BenchmarkResult.from_latencies(
                name="PyWeb WebSocket Frame Roundtrip",
                latencies_ms=ws_latencies,
                duration_sec=total_ws_duration,
                metadata={"frames_exchanged": ws_frames_count},
            )
        )

    finally:
        await server.stop()

    return results


def run_web_benchmark_sync(num_requests: int = 500, concurrency: int = 5) -> List[BenchmarkResult]:
    return asyncio.run(benchmark_pyweb(num_requests=num_requests, concurrency=concurrency))
