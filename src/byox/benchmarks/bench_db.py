"""PyDB Paged B-Tree & Query Engine Benchmark."""

from __future__ import annotations
import os
import tempfile
import time
from typing import List
from pydb.engine import DatabaseEngine
from byox.benchmarks.metrics import BenchmarkResult


def benchmark_pydb(num_rows: int = 1000) -> List[BenchmarkResult]:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, "bench.db")
        engine = DatabaseEngine(db_path)
        engine.execute("CREATE TABLE accounts (id INT, holder TEXT, balance REAL);")

        results: List[BenchmarkResult] = []

        # 1. Bulk Insertion Benchmark
        insert_latencies: List[float] = []
        t0_insert = time.perf_counter()

        for i in range(num_rows):
            sql = f"INSERT INTO accounts VALUES ({i}, 'User_{i}', {round(i * 1.5, 2)});"
            t0 = time.perf_counter()
            engine.execute(sql)
            insert_latencies.append((time.perf_counter() - t0) * 1000.0)

        total_insert_time = time.perf_counter() - t0_insert
        num_pages_allocated = engine.pager.num_pages()

        results.append(
            BenchmarkResult.from_latencies(
                name="PyDB Row Insertion",
                latencies_ms=insert_latencies,
                duration_sec=total_insert_time,
                metadata={
                    "rows_inserted": num_rows,
                    "pages_allocated": num_pages_allocated,
                    "avg_bytes_per_row": round((num_pages_allocated * 4096) / num_rows, 1),
                },
            )
        )

        # 2. Query Execution Benchmark (WHERE equality)
        select_latencies: List[float] = []
        t0_select = time.perf_counter()
        query_samples = 200

        for q in range(query_samples):
            target_id = (q * 5) % num_rows
            sql = f"SELECT id, holder, balance FROM accounts WHERE id = {target_id};"
            t0 = time.perf_counter()
            res = engine.execute(sql)
            select_latencies.append((time.perf_counter() - t0) * 1000.0)
            assert len(res.rows) == 1

        total_select_time = time.perf_counter() - t0_select

        results.append(
            BenchmarkResult.from_latencies(
                name="PyDB SELECT WHERE Query",
                latencies_ms=select_latencies,
                duration_sec=total_select_time,
                metadata={"table_size": num_rows, "queries_executed": query_samples},
            )
        )

        engine.close()
        return results
