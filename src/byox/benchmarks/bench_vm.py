"""PyVM Bytecode Compilation & Execution Throughput Benchmark."""

from __future__ import annotations
import time
from typing import List
from pyvm.assembler import assemble
from pyvm.vm import VirtualMachine
from byox.benchmarks.metrics import BenchmarkResult


def benchmark_pyvm(num_runs: int = 500) -> List[BenchmarkResult]:
    assembly_source = """
        PUSH 10
        STORE n
        PUSH 1
        STORE acc

    LOOP:
        LOAD n
        PUSH 1
        LTE
        JUMP_IF_TRUE END

        LOAD acc
        LOAD n
        MUL
        STORE acc

        LOAD n
        PUSH 1
        SUB
        STORE n

        JUMP LOOP

    END:
        LOAD acc
        HALT
    """

    results: List[BenchmarkResult] = []

    # 1. Two-Pass Assembly Benchmark
    asm_latencies: List[float] = []
    t0_asm = time.perf_counter()

    for _ in range(num_runs):
        t0 = time.perf_counter()
        code = assemble(assembly_source)
        asm_latencies.append((time.perf_counter() - t0) * 1000.0)

    total_asm_time = time.perf_counter() - t0_asm
    results.append(
        BenchmarkResult.from_latencies(
            name="PyVM Two-Pass Assembly",
            latencies_ms=asm_latencies,
            duration_sec=total_asm_time,
            metadata={"programs_assembled": num_runs},
        )
    )

    # 2. Virtual Machine Execution Throughput
    compiled_code = assemble(assembly_source)
    vm = VirtualMachine()
    exec_latencies: List[float] = []
    t0_exec = time.perf_counter()

    for _ in range(num_runs):
        t0 = time.perf_counter()
        res = vm.run(compiled_code)
        exec_latencies.append((time.perf_counter() - t0) * 1000.0)
        assert res == 3628800  # 10!

    total_exec_time = time.perf_counter() - t0_exec
    results.append(
        BenchmarkResult.from_latencies(
            name="PyVM Factorial(10) Execution",
            latencies_ms=exec_latencies,
            duration_sec=total_exec_time,
            metadata={"runs": num_runs, "computed_factorial": 3628800},
        )
    )

    return results
