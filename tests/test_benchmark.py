import pytest
from omniverse.operations.benchmark import (
    OmniverseBenchmarkingSuite,
    BenchmarkMetric,
    BenchmarkSuiteReport
)
from omniverse.core.telemetry import global_event_bus

def test_benchmark_percentile_math():
    suite = OmniverseBenchmarkingSuite()
    # Empty list
    assert suite._calculate_percentile([], 95.0) == 0.0

    # Singleton list
    assert suite._calculate_percentile([12.5], 95.0) == 12.5

    # Known distribution
    values = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
    p50 = suite._calculate_percentile(values, 50.0)
    p95 = suite._calculate_percentile(values, 95.0)
    assert p50 == 50.0
    assert p95 == 100.0

def test_benchmark_pbft_consensus():
    suite = OmniverseBenchmarkingSuite()
    metric = suite.run_pbft_benchmark(iterations=5)
    assert metric.name == "PBFT 4-Phase Federated Consensus"
    assert metric.iterations == 5
    assert metric.avg_latency_ms >= 0.0
    assert metric.throughput_ops_per_sec > 0.0
    assert metric.status == "PASSED"

def test_benchmark_derivatives():
    suite = OmniverseBenchmarkingSuite()
    metric = suite.run_derivatives_benchmark(iterations=20)
    assert "Black-Scholes" in metric.name
    assert metric.iterations == 20
    assert metric.avg_latency_ms >= 0.0
    assert metric.throughput_ops_per_sec > 0.0

def test_benchmark_sar_radar():
    suite = OmniverseBenchmarkingSuite()
    metric = suite.run_sar_benchmark(iterations=5)
    assert "Sentinel-1 SAR" in metric.name
    assert metric.iterations == 5
    assert metric.throughput_ops_per_sec > 0.0

def test_benchmark_settlement():
    suite = OmniverseBenchmarkingSuite()
    metric = suite.run_settlement_benchmark(iterations=10)
    assert "Atomic RTGS" in metric.name
    assert metric.iterations == 10
    assert metric.throughput_ops_per_sec > 0.0

def test_benchmark_llm_arbitrator():
    suite = OmniverseBenchmarkingSuite()
    metric = suite.run_llm_arbitrator_benchmark(iterations=10)
    assert "Hybrid LLM Arbitrator" in metric.name
    assert metric.iterations == 10
    assert metric.throughput_ops_per_sec > 0.0

def test_benchmark_suite_run_all():
    suite = OmniverseBenchmarkingSuite()
    report = suite.run_all(iterations=5)

    assert isinstance(report, BenchmarkSuiteReport)
    assert report.total_benchmarks == 5
    assert len(report.metrics) == 5
    assert report.overall_grade == "INSTITUTIONAL_GRADE_A+"

    table = suite.render_table(report)
    assert "CASHFLOW INFINITY EMPIRICAL BENCHMARK" in table
    assert "PBFT" in table
    assert "Black-Scholes" in table
    assert "Sentinel-1" in table

    # Verify telemetry publication
    events = global_event_bus.get_events()
    names = [e["event_name"] for e in events]
    assert "BENCHMARK_COMPLETED" in names

def test_benchmark_zero_or_negative_iterations_safe():
    suite = OmniverseBenchmarkingSuite()
    # iterations=0 should clamp to >= 1 without ZeroDivisionError
    metric_pbft = suite.run_pbft_benchmark(iterations=0)
    assert metric_pbft.iterations >= 1
    assert metric_pbft.throughput_ops_per_sec > 0.0

    metric_deriv = suite.run_derivatives_benchmark(iterations=-10)
    assert metric_deriv.iterations >= 1

    report_zero = suite.run_all(iterations=0)
    assert report_zero.total_benchmarks == 5

def test_benchmark_percentile_clamping():
    suite = OmniverseBenchmarkingSuite()
    vals = [10.0, 20.0, 30.0]
    # Underflow clamped to 0.0
    assert suite._calculate_percentile(vals, -10.0) == 10.0
    # Overflow clamped to 100.0
    assert suite._calculate_percentile(vals, 150.0) == 30.0

