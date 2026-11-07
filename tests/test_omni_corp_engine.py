# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0
"""
Automated Test Suite for OMNI-CORP Enterprise Engines (tests/test_omni_corp_engine.py)
Verifies:
  1. Spanner TrueTime HLC monotonicity, causal tracking, and skew tolerance
  2. Consistent Hash Ring distribution, replication factor, and rebalancing
  3. Multiplayer CRDT Strong Eventual Consistency (SEC) and fractional sequence editing
  4. PagedAttention KV-Cache block allocation, Radix prefix sharing, and COW forks
  5. Real-Time LinUCB contextual bandit exploration/exploitation and rank-1 updates
  6. Immutable Double-Entry Ledger zero-sum conservation and SHA3-512 chaining
"""

import time
import pytest
import numpy as np

from src.omni_corp_engine import (
    SpannerTrueTimeHLC,
    ConsistentHashRing,
    MultiplayerCRDTDocument,
    PagedAttentionKVBlockManager,
    RealTimeLinUCBRecommender,
    ImmutableDoubleEntryLedger,
)


# ============================================================================
# 1. SPANNER TRUETIME & HYBRID LOGICAL CLOCK TESTS
# ============================================================================
def test_spanner_truetime_hlc_monotonicity():
    clock = SpannerTrueTimeHLC("dc-us-east-1", epsilon_uncertainty_ms=1.5)

    # 1. Bounded uncertainty interval width == 2 * epsilon
    earliest, latest = clock.truetime_now()
    n_early, n_late = clock.now()
    assert n_late - n_early == 2 * clock.epsilon_ns

    # 2. Monotonically increasing sequential timestamps
    ts1 = clock.issue_timestamp()
    ts2 = clock.issue_timestamp()
    ts3 = clock.issue_timestamp()
    assert SpannerTrueTimeHLC.compare_timestamps(ts1, ts2) < 0
    assert SpannerTrueTimeHLC.compare_timestamps(ts2, ts3) < 0
    assert ts1[2] == "dc-us-east-1"

    # 3. Clock skew tolerance: simulated physical time stalling advances logical counter
    clock.last_physical_ns = int(2e18)  # Set in the far future
    clock.logical_counter = 5
    ts_skewed = clock.issue_timestamp(remote_phys_ns=0, remote_logical=0)
    assert ts_skewed[0] == int(2e18)
    assert ts_skewed[1] == 6

    # 4. Causal order preservation across nodes
    node_a = SpannerTrueTimeHLC("node-A")
    node_b = SpannerTrueTimeHLC("node-B")
    ts_a = node_a.issue_timestamp()
    # Node B receives message from Node A with ts_a
    ts_b = node_b.issue_timestamp(remote_phys_ns=ts_a[0], remote_logical=ts_a[1])
    assert SpannerTrueTimeHLC.compare_timestamps(ts_a, ts_b) < 0

    # 5. Negative epsilon uncertainty validation
    with pytest.raises(ValueError, match="non-negative"):
        SpannerTrueTimeHLC("node-invalid", epsilon_uncertainty_ms=-1.0)


# ============================================================================
# 2. CONSISTENT HASH RING TESTS
# ============================================================================
def test_consistent_hash_ring_distribution():
    ring = ConsistentHashRing(vnodes_per_shard=128)
    shards = ["storage-nvme-01", "storage-nvme-02", "storage-nvme-03", "storage-nvme-04"]
    for s in shards:
        ring.add_shard(s)

    # Total virtual nodes on ring
    assert len(ring.ring_keys) == 128 * 4
    assert len(ring.nodes) == 4

    # 1. Deterministic lookup
    node1 = ring.get_node("user_partition_key_8841")
    node2 = ring.get_node("user_partition_key_8841")
    assert node1 == node2
    assert node1 in shards

    # 2. Preference list returns k distinct replicas
    pref_list = ring.get_preference_list("tenant_org_9921", replication_factor=3)
    assert len(pref_list) == 3
    assert len(set(pref_list)) == 3  # All distinct

    # 3. Preference list with replication factor > total shards does not hang
    all_replicas = ring.get_preference_list("test_key", replication_factor=10)
    assert len(all_replicas) == 4
    assert set(all_replicas) == set(shards)

    # 4. Zero and negative replication factor cleanly return empty list
    assert ring.get_preference_list("test_key", replication_factor=0) == []
    assert ring.get_preference_list("test_key", replication_factor=-2) == []

    # 5. Shard removal rebalances keys
    ring.remove_shard("storage-nvme-01")
    assert len(ring.nodes) == 3
    assert len(ring.ring_keys) == 128 * 3
    assert "storage-nvme-01" not in ring.nodes
    # Querying after removal returns remaining active shards
    assert ring.get_node("user_partition_key_8841") in ring.nodes


def test_consistent_hash_ring_empty_raises():
    ring = ConsistentHashRing()
    with pytest.raises(RuntimeError):
        ring.get_node("key")
    assert ring.get_preference_list("key") == []


# ============================================================================
# 3. MULTIPLAYER CRDT DOCUMENT TESTS
# ============================================================================
def test_multiplayer_crdt_strong_eventual_consistency():
    clock_us = SpannerTrueTimeHLC("aws-us-east-1")
    clock_eu = SpannerTrueTimeHLC("gcp-europe-west1")
    doc_us = MultiplayerCRDTDocument(clock_us)
    doc_eu = MultiplayerCRDTDocument(clock_eu)

    # 1. Independent local edits
    doc_us.mutate("theme.background", "#1E293B")
    doc_us.mutate("layout.sidebar", "collapsed")
    doc_eu.mutate("theme.background", "#0F172A")
    doc_eu.mutate("layout.header", "sticky")

    # 2. Bidirectional state merge (Commutativity & SEC)
    doc_us.merge_remote(doc_eu.registers)
    doc_eu.merge_remote(doc_us.registers)

    view_us = doc_us.materialize_view()
    view_eu = doc_eu.materialize_view()
    assert view_us == view_eu
    assert view_us["layout.sidebar"] == "collapsed"
    assert view_us["layout.header"] == "sticky"
    assert "theme.background" in view_us

    # 3. Idempotency: merging same state again causes zero side-effects
    prev_view = dict(view_us)
    doc_us.merge_remote(doc_eu.registers)
    assert doc_us.materialize_view() == prev_view

    # 4. Tombstone deletion
    doc_us.delete("layout.sidebar")
    assert "layout.sidebar" not in doc_us.materialize_view()
    doc_eu.merge_remote(doc_us.registers)
    assert "layout.sidebar" not in doc_eu.materialize_view()


def test_multiplayer_crdt_fractional_sequence_editing():
    doc = MultiplayerCRDTDocument()
    id1 = doc.insert(0, "A")
    id2 = doc.insert(1, "C")
    # Insert B between A and C
    id3 = doc.insert(1, "B")
    assert doc.get_text() == "ABC"

    # Delete 'B' at logical index 1
    deleted = doc.delete_at(1)
    assert deleted is True
    assert doc.get_text() == "AC"

    # Insert at end
    doc.insert(2, "D")
    assert doc.get_text() == "ACD"


# ============================================================================
# 4. PAGEDATTENTION KV-CACHE BLOCK MANAGER TESTS
# ============================================================================
def test_paged_attention_kv_block_manager():
    mgr = PagedAttentionKVBlockManager(total_hbm_blocks=16, tokens_per_block=4)

    # 1. Basic allocation
    prompt_tokens = [f"t_{i}" for i in range(12)]  # 3 blocks of 4 tokens
    res1 = mgr.allocate_sequence("req-01", prompt_tokens)
    assert len(res1["physical_hbm_pages"]) == 3
    assert res1["zero_copy_prefix_hits"] == 0
    assert res1["hbm_pool_utilization_pct"] == round(100.0 * 3 / 16, 2)

    # 2. Radix prefix sharing: identical 12-token prompt for req-02
    res2 = mgr.allocate_sequence("req-02", prompt_tokens + ["q1", "q2"])
    # First 3 blocks should be shared (hits == 3), plus 1 new block for remaining 2 tokens
    assert res2["zero_copy_prefix_hits"] == 3
    assert len(res2["physical_hbm_pages"]) == 4
    # Blocks shared between req-01 and req-02 have ref_count == 2
    for blk in res1["physical_hbm_pages"]:
        assert mgr.block_ref_counts[blk] == 2

    # 3. Copy-on-write fork
    forked_pages = mgr.fork_sequence("req-01", "req-forked")
    assert forked_pages == res1["physical_hbm_pages"]
    for blk in forked_pages:
        assert mgr.block_ref_counts[blk] == 3

    # Append token to forked sequence triggers COW
    appended_blk = mgr.append_token("req-forked", "new_token")
    assert appended_blk in mgr.seq_page_tables["req-forked"]

    # 4. Free sequence restores blocks to free pool
    mgr.free_sequence("req-01")
    mgr.free_sequence("req-02")
    mgr.free_sequence("req-forked")
    assert len(mgr.free_blocks) == 16


def test_paged_attention_pool_exhaustion():
    mgr = PagedAttentionKVBlockManager(total_hbm_blocks=2, tokens_per_block=4)
    mgr.allocate_sequence("req-1", ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"])
    with pytest.raises(MemoryError, match="KV-Cache Pool Exhausted"):
        mgr.allocate_sequence("req-2", ["extra1", "extra2"])


# ============================================================================
# 5. LINUCB CONTEXTUAL BANDIT RECOMMENDER TESTS
# ============================================================================
def test_linucb_recommender_exploration_exploitation():
    bandit = RealTimeLinUCBRecommender(candidate_items=4, embedding_dim=3, alpha_explore=0.5)

    context = np.array([1.0, 0.0, 0.5])
    arm, ucb = bandit.rank_item(context)
    assert 0 <= arm < 4
    assert isinstance(ucb, float)
    assert bandit.select_arm(context) == arm

    # Repeated high rewards on arm 2 should bias selection towards arm 2
    for _ in range(25):
        bandit.ingest_streaming_feedback(arm=2, user_context_vec=context, watch_reward=5.0)

    favored_arm, favored_ucb = bandit.rank_item(context)
    assert favored_arm == 2

    # Updating with invalid dimension raises ValueError
    with pytest.raises(ValueError, match="Context dimension mismatch"):
        bandit.rank_item(np.array([1.0, 2.0]))

    with pytest.raises(ValueError, match="Context dimension mismatch"):
        bandit.ingest_streaming_feedback(0, np.array([1.0]), 1.0)


# ============================================================================
# 6. IMMUTABLE DOUBLE-ENTRY FINANCIAL LEDGER TESTS
# ============================================================================
def test_immutable_double_entry_ledger_invariants():
    ledger = ImmutableDoubleEntryLedger()

    # 1. 2-leg transfer: debit decreases, credit increases
    tx1 = ledger.commit_transfer(
        idempotency_key="tx-uuid-001",
        debit_account="treasury:reserve",
        credit_account="merchant:alpha",
        amount_cents=100_000,
    )
    assert tx1["amount_cents"] == 100_000
    assert tx1["zero_sum_invariant_verified"] is True
    assert tx1["idempotent_cache_hit"] is False
    assert ledger.get_balance("treasury:reserve") == -100_000
    assert ledger.get_balance("merchant:alpha") == 100_000
    assert ledger.verify_ledger_invariants() is True

    # 2. Idempotent retry: exact same key returns cached result without double charging
    tx1_retry = ledger.commit_transfer(
        idempotency_key="tx-uuid-001",
        debit_account="treasury:reserve",
        credit_account="merchant:alpha",
        amount_cents=100_000,
    )
    assert tx1_retry["idempotent_cache_hit"] is True
    assert ledger.get_balance("treasury:reserve") == -100_000
    assert ledger.get_balance("merchant:alpha") == 100_000

    # 3. Negative or zero amount rejection
    with pytest.raises(ValueError, match="positive integer"):
        ledger.commit_transfer("tx-bad-1", "acct1", "acct2", -50)
    with pytest.raises(ValueError, match="positive integer"):
        ledger.commit_transfer("tx-bad-2", "acct1", "acct2", 0)

    # 4. Multi-leg atomic transfer
    multileg_tx = ledger.commit_multileg_transfer(
        idempotency_key="tx-multileg-002",
        legs=[
            ("customer:bob", -5000),
            ("merchant:beta", 4750),
            ("fee:processing", 250),
        ],
    )
    assert multileg_tx["zero_sum_invariant_verified"] is True
    assert ledger.get_balance("customer:bob") == -5000
    assert ledger.get_balance("merchant:beta") == 4750
    assert ledger.get_balance("fee:processing") == 250
    assert ledger.verify_ledger_invariants() is True

    # 5. Invalid multi-leg transfer (non-zero sum) raises ValueError
    with pytest.raises(ValueError, match="zero sum"):
        ledger.commit_multileg_transfer(
            idempotency_key="tx-bad-multi",
            legs=[("a", -100), ("b", 50)],
        )

    # 6. SHA3-512 chain verification: chain head is a 128-character hex digest
    assert len(ledger.chain_head_hash) == 128
    assert len(ledger.journal) == 2
