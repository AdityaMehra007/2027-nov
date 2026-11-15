"""Unified Benchmark Runner across all 10 BYOX systems."""

from __future__ import annotations
import json
import os
import time
from typing import Any, Dict, List

from byox.benchmarks.bench_db import benchmark_pydb
from byox.benchmarks.bench_git import benchmark_pygit
from byox.benchmarks.bench_redis import run_redis_benchmark_sync
from byox.benchmarks.bench_shell import benchmark_pyshell
from byox.benchmarks.bench_transformer import benchmark_pytransformer
from byox.benchmarks.bench_web import run_web_benchmark_sync
from byox.benchmarks.bench_chain import benchmark_pychain
from byox.benchmarks.bench_search import benchmark_pysearch
from byox.benchmarks.bench_vm import benchmark_pyvm
from byox.benchmarks.bench_controlplane import benchmark_pycontrolplane
from byox.benchmarks.metrics import BenchmarkResult


def run_all_benchmarks(
    redis_reqs: int = 500,
    web_reqs: int = 300,
    db_rows: int = 500,
    git_files: int = 100,
    shell_cmds: int = 300,
    chain_txs: int = 100,
    search_docs: int = 300,
    vm_runs: int = 300,
    cp_reqs: int = 150,
) -> Dict[str, Any]:
    print("[*] Running BYOX Unified 10-Engine Benchmark Suite...")
    all_results: List[BenchmarkResult] = []
    t_start = time.perf_counter()

    # 1. PyRedis
    print("  [1/10] -> Benchmarking PyRedis (In-Memory KV)...")
    r_res = run_redis_benchmark_sync(num_requests=redis_reqs, concurrency=10)
    all_results.extend(r_res)

    # 2. PyDB
    print("  [2/10] -> Benchmarking PyDB (4KB B-Tree SQL)...")
    db_res = benchmark_pydb(num_rows=db_rows)
    all_results.extend(db_res)

    # 3. PyWeb
    print("  [3/10] -> Benchmarking PyWeb (HTTP/1.1 & WebSocket)...")
    web_res = run_web_benchmark_sync(num_requests=web_reqs, concurrency=5)
    all_results.extend(web_res)

    # 4. PyGit
    print("  [4/10] -> Benchmarking PyGit (VCS Objects & Merkle Tree)...")
    git_res = benchmark_pygit(num_files=git_files)
    all_results.extend(git_res)

    # 5. PyShell
    print("  [5/10] -> Benchmarking PyShell (Execution & Redirection)...")
    shell_res = benchmark_pyshell(num_commands=shell_cmds)
    all_results.extend(shell_res)

    # 6. PyTransformer
    print("  [6/10] -> Benchmarking PyTransformer (Autograd & Attention)...")
    tf_res = benchmark_pytransformer()
    all_results.extend(tf_res)

    # 7. PyChain
    print("  [7/10] -> Benchmarking PyChain (Proof-of-Work Blockchain)...")
    chain_res = benchmark_pychain(num_txs=chain_txs, difficulty=1)
    all_results.extend(chain_res)

    # 8. PySearch
    print("  [8/10] -> Benchmarking PySearch (BM25 Inverted Index)...")
    search_res = benchmark_pysearch(num_docs=search_docs, num_queries=150)
    all_results.extend(search_res)

    # 9. PyVM
    print("  [9/10] -> Benchmarking PyVM (Bytecode Assembler & Execution)...")
    vm_res = benchmark_pyvm(num_runs=vm_runs)
    all_results.extend(vm_res)

    # 10. PyControlPlane
    print("  [10/10] -> Benchmarking PyControlPlane (Telemetry, Cache, Audit)...")
    cp_res = benchmark_pycontrolplane(num_requests=cp_reqs)
    all_results.extend(cp_res)

    total_wall_time = time.perf_counter() - t_start
    print(f"[*] All 10 BYOX Benchmarks complete in {total_wall_time:.2f}s!")

    output_data = {
        "timestamp": time.time(),
        "wall_time_sec": round(total_wall_time, 3),
        "total_benchmarks": len(all_results),
        "results": [r.to_dict() for r in all_results],
    }

    # Save to JSON
    os.makedirs("data", exist_ok=True)
    json_path = os.path.join("data", "byox_benchmark_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    # Save to Markdown
    os.makedirs("docs", exist_ok=True)
    md_path = os.path.join("docs", "byox_benchmark_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# BYOX 10-Engine Multi-System Benchmark Report\n\n")
        f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}  \n")
        f.write(f"**Total Run Time:** {total_wall_time:.2f} seconds  \n")
        f.write(f"**Engines Evaluated:** 10 Systems (22 Benchmarks)\n\n")
        f.write("| Benchmark Target | Total Ops | Duration (s) | Throughput (ops/s) | p50 (ms) | p95 (ms) | p99 (ms) |\n")
        f.write("|:---|:---:|:---:|:---:|:---:|:---:|:---:|\n")
        for r in all_results:
            f.write(
                f"| **{r.name}** | {r.total_ops:,} | {r.duration_sec:.3f} | {r.ops_per_sec:,.1f} | {r.p50_ms:.2f} | {r.p95_ms:.2f} | {r.p99_ms:.2f} |\n"
            )

    return output_data


if __name__ == "__main__":
    run_all_benchmarks()
