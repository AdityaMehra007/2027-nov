"""PyRedis Concurrency, Throughput, and Pipelining Benchmark."""

from __future__ import annotations
import asyncio
import tempfile
import time
from typing import List
from pyredis.server import RedisServer
from byox.benchmarks.metrics import BenchmarkResult


async def benchmark_redis(
    num_requests: int = 2000,
    concurrency: int = 20,
) -> List[BenchmarkResult]:
    with tempfile.TemporaryDirectory() as tmp:
        server = RedisServer(host="127.0.0.1", port=0)
        await server.start()
        port = server.actual_port

        results: List[BenchmarkResult] = []

        try:
            # 1. Concurrent SET/GET benchmark
            latencies_ms: List[float] = []
            reqs_per_worker = num_requests // concurrency

            async def worker(worker_id: int):
                r, w = await asyncio.open_connection("127.0.0.1", port)
                for i in range(reqs_per_worker):
                    key = f"key:{worker_id}:{i}"
                    val = f"val:{worker_id}:{i}"
                    cmd = f"*3\r\n$3\r\nSET\r\n${len(key)}\r\n{key}\r\n${len(val)}\r\n{val}\r\n".encode()

                    t0 = time.perf_counter()
                    w.write(cmd)
                    await w.drain()
                    resp = await r.read(128)
                    elapsed = (time.perf_counter() - t0) * 1000.0
                    latencies_ms.append(elapsed)

                w.close()
                await w.wait_closed()

            t_start = time.perf_counter()
            tasks = [worker(w_id) for w_id in range(concurrency)]
            await asyncio.gather(*tasks)
            total_duration = time.perf_counter() - t_start

            results.append(
                BenchmarkResult.from_latencies(
                    name="PyRedis Concurrent SET",
                    latencies_ms=latencies_ms,
                    duration_sec=total_duration,
                    metadata={"concurrency": concurrency, "key_count": len(latencies_ms)},
                )
            )

            # 2. Pipelined throughput benchmark
            pipeline_latencies: List[float] = []
            pipe_batch_size = 50
            num_batches = num_requests // pipe_batch_size

            r_pipe, w_pipe = await asyncio.open_connection("127.0.0.1", port)
            t_pipe_start = time.perf_counter()

            for b in range(num_batches):
                payload = bytearray()
                for i in range(pipe_batch_size):
                    k = f"pipe:{b}:{i}"
                    payload.extend(f"*2\r\n$3\r\nGET\r\n${len(k)}\r\n{k}\r\n".encode())

                t0 = time.perf_counter()
                w_pipe.write(payload)
                await w_pipe.drain()

                # Read all responses
                bytes_expected = len(b"$-1\r\n") * pipe_batch_size
                received = 0
                while received < bytes_expected:
                    chunk = await r_pipe.read(4096)
                    if not chunk:
                        break
                    received += len(chunk)

                elapsed = (time.perf_counter() - t0) * 1000.0
                pipeline_latencies.append(elapsed)

            pipe_duration = time.perf_counter() - t_pipe_start
            w_pipe.close()
            await w_pipe.wait_closed()

            results.append(
                BenchmarkResult.from_latencies(
                    name="PyRedis Pipelined GET (50-op batch)",
                    latencies_ms=pipeline_latencies,
                    duration_sec=pipe_duration,
                    metadata={
                        "batch_size": pipe_batch_size,
                        "total_pipelined_commands": num_batches * pipe_batch_size,
                    },
                )
            )

        finally:
            await server.stop()

        return results


def run_redis_benchmark_sync(num_requests: int = 1000, concurrency: int = 10) -> List[BenchmarkResult]:
    return asyncio.run(benchmark_redis(num_requests=num_requests, concurrency=concurrency))
