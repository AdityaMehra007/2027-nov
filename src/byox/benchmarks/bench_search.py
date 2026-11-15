"""PySearch Inverted Index & BM25 Ranking Benchmark."""

from __future__ import annotations
import time
from typing import List
from pysearch.index import InvertedIndex
from pysearch.bm25 import BM25Ranker
from byox.benchmarks.metrics import BenchmarkResult


def benchmark_pysearch(num_docs: int = 500, num_queries: int = 200) -> List[BenchmarkResult]:
    index = InvertedIndex()
    results: List[BenchmarkResult] = []

    # 1. Document Ingestion & Stemmed Inverted Posting
    ingest_latencies: List[float] = []
    sample_corpus = [
        "Distributed database consistency models and raft consensus algorithms",
        "High performance neural network inference runtime with scalar autograd",
        "Zero dependency python socket server with RFC 6455 websocket framing",
        "Byzantine fault tolerant multi agent swarm coordination and cryptographic ledger",
        "Probabilistic BM25 Okapi information retrieval and suffix stemming index",
    ]

    t0_ingest = time.perf_counter()
    for i in range(num_docs):
        text = f"{sample_corpus[i % len(sample_corpus)]} doc_unique_token_{i}"
        t0 = time.perf_counter()
        index.add_document(i, text, {"doc_num": i})
        ingest_latencies.append((time.perf_counter() - t0) * 1000.0)

    total_ingest_time = time.perf_counter() - t0_ingest
    results.append(
        BenchmarkResult.from_latencies(
            name="PySearch Document Indexing",
            latencies_ms=ingest_latencies,
            duration_sec=total_ingest_time,
            metadata={"docs_indexed": num_docs, "total_postings": len(index.postings)},
        )
    )

    # 2. BM25 Query Evaluation
    ranker = BM25Ranker(index)
    query_latencies: List[float] = []
    queries = [
        "distributed consensus raft",
        "neural network inference autograd",
        "python websocket server framing",
        "byzantine fault swarm ledger",
        "information retrieval stemming",
    ]

    t0_queries = time.perf_counter()
    for q in range(num_queries):
        query = queries[q % len(queries)]
        t0 = time.perf_counter()
        ranked = ranker.search(query, top_k=5)
        query_latencies.append((time.perf_counter() - t0) * 1000.0)
        assert len(ranked) > 0

    total_query_time = time.perf_counter() - t0_queries
    results.append(
        BenchmarkResult.from_latencies(
            name="PySearch BM25 Ranking Queries",
            latencies_ms=query_latencies,
            duration_sec=total_query_time,
            metadata={"queries_evaluated": num_queries, "top_k": 5},
        )
    )

    return results
