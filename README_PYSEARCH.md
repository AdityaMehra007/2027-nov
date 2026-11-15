# `src/pysearch` - Zero-Dependency Full-Text Search and BM25 Ranking Engine

A high-performance full-text search engine implemented purely using Python's standard library (`math`, `re`, `dataclasses`, `typing`).

## Architecture & Capabilities

1. **Tokenizer & Normalizer (`src/pysearch/tokenizer.py`)**:
   - Case normalization and alphanumeric token extraction.
   - Comprehensive stopword filtering.
   - Algorithmic suffix stemming (`stem()`) for plurals, verb conjugations, and affix reduction.

2. **Inverted Index (`src/pysearch/index.py`)**:
   - Term-to-document inverted posting lists with term frequencies (`tf`).
   - Dynamic document length tracking and global average document length (`avgdl`).
   - Support for dynamic indexing and document deletion.

3. **BM25 Okapi Scoring (`src/pysearch/bm25.py`)**:
   - Classical probabilistic information retrieval model:
     $$IDF(q_i) = \ln\left(1 + \frac{N - n(q_i) + 0.5}{n(q_i) + 0.5}\right)$$
     $$Score(D, Q) = \sum_{q_i \in Q} IDF(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
   - Parameter calibration ($k_1=1.5, b=0.75$) with term saturation and document length normalization.

4. **Boolean Filtering (`src/pysearch/query.py`)**:
   - Set-theoretic boolean query operations: `search_and`, `search_or`, and `search_not`.

## Test Suite

```bash
python -m pytest tests/test_pysearch.py -v
```
All 5 test specifications pass with 100% fidelity.
