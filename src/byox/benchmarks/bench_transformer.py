"""PyTransformer Autograd & Inference Generation Benchmark."""

from __future__ import annotations
import time
from typing import List
from pytransformer.autograd import Value
from pytransformer.model import MiniTransformer
from pytransformer.tokenizer import CharacterTokenizer
from byox.benchmarks.metrics import BenchmarkResult


def benchmark_pytransformer() -> List[BenchmarkResult]:
    results: List[BenchmarkResult] = []

    # 1. Autograd Backpropagation Benchmark (Deep Graph)
    autograd_latencies: List[float] = []
    t0_autograd = time.perf_counter()
    num_graphs = 200

    for _ in range(num_graphs):
        # Build 10-layer computational graph
        x = Value(1.5)
        curr = x
        for _ in range(8):
            curr = (curr * 1.05 + Value(0.2)).relu()

        t0 = time.perf_counter()
        curr.backward()
        autograd_latencies.append((time.perf_counter() - t0) * 1000.0)

    total_autograd_time = time.perf_counter() - t0_autograd

    results.append(
        BenchmarkResult.from_latencies(
            name="PyTransformer Autograd Graph Backprop",
            latencies_ms=autograd_latencies,
            duration_sec=total_autograd_time,
            metadata={"graph_evaluations": num_graphs, "graph_depth": 8},
        )
    )

    # 2. Autoregressive Generation Latency Benchmark
    corpus = "The quick brown fox jumps over the lazy dog."
    tok = CharacterTokenizer(corpus)
    model = MiniTransformer(
        vocab_size=tok.vocab_size,
        embed_dim=16,
        num_heads=2,
        context_len=16,
    )

    prompt = "The"
    input_ids = tok.encode(prompt)

    token_latencies: List[float] = []
    tokens_to_generate = 15
    curr_tokens = list(input_ids)
    t0_gen = time.perf_counter()

    for _ in range(tokens_to_generate):
        t0 = time.perf_counter()
        logits = model.forward(curr_tokens)
        last_logits = logits[-1]
        best_id = 0
        best_val = last_logits[0].data
        for i in range(1, len(last_logits)):
            if last_logits[i].data > best_val:
                best_val = last_logits[i].data
                best_id = i
        curr_tokens.append(best_id)
        token_latencies.append((time.perf_counter() - t0) * 1000.0)

    total_gen_time = time.perf_counter() - t0_gen

    results.append(
        BenchmarkResult.from_latencies(
            name="PyTransformer Autoregressive Token Generation",
            latencies_ms=token_latencies,
            duration_sec=total_gen_time,
            metadata={
                "tokens_generated": tokens_to_generate,
                "tokens_per_sec": round(tokens_to_generate / max(total_gen_time, 0.001), 2),
            },
        )
    )

    return results
