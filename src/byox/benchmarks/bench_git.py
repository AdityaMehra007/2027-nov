"""PyGit Object Hashing, Index Staging, and Tree Serialization Benchmark."""

from __future__ import annotations
import os
import tempfile
import time
from typing import List
from pygit.commands import cmd_add, cmd_commit, cmd_init, cmd_log
from pygit.objects import Blob, hash_object
from byox.benchmarks.metrics import BenchmarkResult


def benchmark_pygit(num_files: int = 150) -> List[BenchmarkResult]:
    with tempfile.TemporaryDirectory() as tmp:
        old_cwd = os.getcwd()
        os.chdir(tmp)
        results: List[BenchmarkResult] = []

        try:
            repo = cmd_init(".")

            # 1. Raw Object Hashing & zlib Storage Benchmark
            blob_latencies: List[float] = []
            t0_blob = time.perf_counter()

            for i in range(num_files):
                payload = f"content of file {i} with some sample lines of code\n" * 10
                blob = Blob(payload.encode("utf-8"))
                t0 = time.perf_counter()
                sha = hash_object(repo.git_dir, blob, write=True)
                blob_latencies.append((time.perf_counter() - t0) * 1000.0)

            total_blob_time = time.perf_counter() - t0_blob

            results.append(
                BenchmarkResult.from_latencies(
                    name="PyGit Object Hashing & zlib Compression",
                    latencies_ms=blob_latencies,
                    duration_sec=total_blob_time,
                    metadata={"objects_created": num_files},
                )
            )

            # 2. File Staging & Index Serialization Benchmark
            # Create files on disk
            for i in range(num_files):
                sub = f"sub_{i % 5}"
                os.makedirs(sub, exist_ok=True)
                with open(os.path.join(sub, f"test_{i}.txt"), "w") as f:
                    f.write(f"Sample data for file {i}\n")

            t0_add = time.perf_counter()
            cmd_add([f"sub_{k}" for k in range(5)])
            add_duration = time.perf_counter() - t0_add

            results.append(
                BenchmarkResult(
                    name="PyGit Index Staging (150 files)",
                    total_ops=num_files,
                    duration_sec=round(add_duration, 4),
                    ops_per_sec=round(num_files / max(add_duration, 0.0001), 2),
                    p50_ms=round(add_duration * 1000.0 / num_files, 3),
                    p95_ms=round(add_duration * 1000.0 / num_files, 3),
                    p99_ms=round(add_duration * 1000.0 / num_files, 3),
                    min_ms=0.0,
                    max_ms=round(add_duration * 1000.0, 3),
                    mean_ms=round(add_duration * 1000.0 / num_files, 3),
                    metadata={"files_staged": num_files},
                )
            )

            # 3. Tree Generation & Commit Benchmark
            t0_commit = time.perf_counter()
            commit_sha = cmd_commit("Benchmark commit with 150 files")
            commit_duration = time.perf_counter() - t0_commit

            results.append(
                BenchmarkResult(
                    name="PyGit Tree Construction & Commit",
                    total_ops=1,
                    duration_sec=round(commit_duration, 4),
                    ops_per_sec=round(1.0 / max(commit_duration, 0.0001), 2),
                    p50_ms=round(commit_duration * 1000.0, 3),
                    p95_ms=round(commit_duration * 1000.0, 3),
                    p99_ms=round(commit_duration * 1000.0, 3),
                    min_ms=round(commit_duration * 1000.0, 3),
                    max_ms=round(commit_duration * 1000.0, 3),
                    mean_ms=round(commit_duration * 1000.0, 3),
                    metadata={"commit_sha": commit_sha, "files_in_tree": num_files},
                )
            )

        finally:
            os.chdir(old_cwd)

        return results
