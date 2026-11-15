# `src/pychain` - Zero-Dependency Proof-of-Work Blockchain Engine

Built from scratch using only Python's standard library (`hashlib`, `json`, `time`, `dataclasses`).

## Architecture & Features

1. **Cryptographic Transactions (`src/pychain/transaction.py`)**:
   - Explicit sender, recipient, amount, fee, and timestamp.
   - Deterministic SHA-256 transaction IDs.
   - Coinbase transaction identification for block rewards.

2. **Merkle Trees & Blocks (`src/pychain/block.py`)**:
   - Pairwise SHA-256 Merkle root computation with odd-element handling.
   - Proof-of-Work consensus algorithm with configurable mining difficulty.
   - Cryptographic header verification.

3. **Blockchain & Consensus (`src/pychain/blockchain.py`)**:
   - Genesis block generation.
   - Transaction mempool and balance verification (UTXO-style double-spend prevention).
   - Longest valid chain consensus resolution across competing distributed peers.
   - Complete block-by-block cryptographic audit (`is_valid_chain()`).

## Test Suite

```bash
python -m pytest tests/test_pychain.py -v
```
All 8 test specifications pass with 100% fidelity.
