use omni_core::{AtomicCircuitBreaker, AtomicTokenBucket, TamperEvidentAuditLedger};

#[test]
fn test_01_lock_free_token_bucket_exhaustion_and_bounds() {
    let limiter = AtomicTokenBucket::new(5, 1);
    assert!(limiter.try_acquire(3));
    assert!(limiter.try_acquire(2));
    // Bucket is now at 0 tokens; acquiring 1 more immediately must return false
    assert!(!limiter.try_acquire(1));
}

#[test]
fn test_02_circuit_breaker_trips_and_recovers() {
    let breaker = AtomicCircuitBreaker::new(3);
    assert!(breaker.allow_execution());
    breaker.record_failure();
    breaker.record_failure();
    assert!(breaker.allow_execution());
    breaker.record_failure();
    // Threshold (3) reached -> Circuit Breaker is now OPEN
    assert!(!breaker.allow_execution());
    // Recording success resets state to CLOSED
    breaker.record_success();
    assert!(breaker.allow_execution());
}

#[test]
fn test_03_idempotency_and_blake3_hash_chain_across_all_100_projects() {
    let ledger = TamperEvidentAuditLedger::new();

    for project_id in 1..=100 {
        let key = format!("idem-proj-{:03}", project_id);
        let first = ledger.append_sealed_entry(&key, project_id, "sovereign-tenant", "payload-v1");
        // Duplicate call with same idempotency key must return the exact same record_id and seal
        let duplicate =
            ledger.append_sealed_entry(&key, project_id, "sovereign-tenant", "payload-v1");
        assert_eq!(first.record_id, duplicate.record_id);
        assert_eq!(first.blake3_seal, duplicate.blake3_seal);
        assert_eq!(first.sequence_no, project_id as u64);
    }

    let verification = ledger.verify_entire_chain();
    assert!(verification.chain_intact);
    assert_eq!(verification.total_entries_verified, 100);
}
