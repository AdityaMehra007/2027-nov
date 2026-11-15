"""PyShell Command Dispatch & Redirection Benchmark."""

from __future__ import annotations
import os
import tempfile
import time
from typing import List
from pyshell.executor import ShellExecutor
from byox.benchmarks.metrics import BenchmarkResult


def benchmark_pyshell(num_commands: int = 500) -> List[BenchmarkResult]:
    with tempfile.TemporaryDirectory() as tmp:
        old_cwd = os.getcwd()
        os.chdir(tmp)
        results: List[BenchmarkResult] = []

        try:
            executor = ShellExecutor()

            # 1. Built-in command evaluation benchmark
            builtin_latencies: List[float] = []
            t0_builtin = time.perf_counter()

            for i in range(num_commands):
                cmd = f"echo 'benchmarking_token_{i}'"
                t0 = time.perf_counter()
                out = executor.run_line(cmd)
                builtin_latencies.append((time.perf_counter() - t0) * 1000.0)

            total_builtin_time = time.perf_counter() - t0_builtin

            results.append(
                BenchmarkResult.from_latencies(
                    name="PyShell Built-in Execution (echo)",
                    latencies_ms=builtin_latencies,
                    duration_sec=total_builtin_time,
                    metadata={"iterations": num_commands},
                )
            )

            # 2. File Redirection Benchmark
            redirect_latencies: List[float] = []
            t0_redir = time.perf_counter()

            for i in range(num_commands):
                cmd = f"echo 'data line {i}' >> output_log.txt"
                t0 = time.perf_counter()
                executor.run_line(cmd)
                redirect_latencies.append((time.perf_counter() - t0) * 1000.0)

            total_redir_time = time.perf_counter() - t0_redir

            results.append(
                BenchmarkResult.from_latencies(
                    name="PyShell File Redirection (>>)",
                    latencies_ms=redirect_latencies,
                    duration_sec=total_redir_time,
                    metadata={"lines_written": num_commands},
                )
            )

        finally:
            os.chdir(old_cwd)

        return results
