pub mod consensus;
pub mod crypto;
pub mod telemetry;
pub use telemetry::GLOBAL_TELEMETRY;

use chrono::{DateTime, Utc};
use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use std::sync::atomic::{AtomicU64, AtomicU8, Ordering};
use std::sync::Mutex;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use uuid::Uuid;

pub const GENESIS_HASH: &str =
    "GENESIS_00000000000000000000000000000000000000000000000000000000";

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CoreAuditEntry {
    pub record_id: Uuid,
    pub sequence_no: u64,
    pub project_id: u32,
    pub tenant_id: String,
    pub payload_summary: String,
    pub previous_hash: String,
    pub blake3_seal: String,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChainVerificationReport {
    pub total_entries_verified: usize,
    pub chain_intact: bool,
    pub head_blake3_seal: String,
}

/// Lock-Free Atomic Token Bucket Rate Limiter with Nanosecond Refill CAS Loop
pub struct AtomicTokenBucket {
    capacity: u64,
    refill_per_sec: u64,
    tokens: AtomicU64,
    last_refill_ns: AtomicU64,
}

impl AtomicTokenBucket {
    pub fn new(capacity: u64, refill_per_sec: u64) -> Self {
        Self {
            capacity,
            refill_per_sec,
            tokens: AtomicU64::new(capacity),
            last_refill_ns: AtomicU64::new(Self::now_ns()),
        }
    }

    #[inline(always)]
    pub fn now_ns() -> u64 {
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or(Duration::ZERO)
            .as_nanos() as u64
    }

    pub fn try_acquire(&self, cost: u64) -> bool {
        let now = Self::now_ns();
        let last = self.last_refill_ns.load(Ordering::Acquire);
        let elapsed = now.saturating_sub(last);

        if elapsed > 0 {
            let added = (elapsed as u128 * self.refill_per_sec as u128) / 1_000_000_000;
            if added > 0
                && self
                    .last_refill_ns
                    .compare_exchange(last, now, Ordering::AcqRel, Ordering::Relaxed)
                    .is_ok()
            {
                let mut cur = self.tokens.load(Ordering::Relaxed);
                loop {
                    let next = (cur + added as u64).min(self.capacity);
                    match self.tokens.compare_exchange_weak(
                        cur,
                        next,
                        Ordering::AcqRel,
                        Ordering::Relaxed,
                    ) {
                        Ok(_) => break,
                        Err(actual) => cur = actual,
                    }
                }
            }
        }

        let mut cur = self.tokens.load(Ordering::Acquire);
        loop {
            if cur < cost {
                return false;
            }
            match self.tokens.compare_exchange_weak(
                cur,
                cur - cost,
                Ordering::AcqRel,
                Ordering::Relaxed,
            ) {
                Ok(_) => return true,
                Err(actual) => cur = actual,
            }
        }
    }
}

/// Lock-Free 3-State Circuit Breaker (0 = Closed, 1 = Open, 2 = HalfOpen)
pub struct AtomicCircuitBreaker {
    state: AtomicU8,
    failures: AtomicU64,
    threshold: u64,
}

impl AtomicCircuitBreaker {
    pub fn new(threshold: u64) -> Self {
        Self {
            state: AtomicU8::new(0),
            failures: AtomicU64::new(0),
            threshold,
        }
    }

    pub fn allow_execution(&self) -> bool {
        self.state.load(Ordering::Acquire) != 1
    }

    pub fn record_success(&self) {
        self.failures.store(0, Ordering::Release);
        self.state.store(0, Ordering::Release);
    }

    pub fn record_failure(&self) {
        let count = self.failures.fetch_add(1, Ordering::AcqRel) + 1;
        if count >= self.threshold {
            self.state.store(1, Ordering::Release);
        }
    }
}

/// Append-Only Tamper-Evident BLAKE3 Hash-Chain Audit Ledger & Idempotency Cache
pub struct TamperEvidentAuditLedger {
    chain: Mutex<Vec<CoreAuditEntry>>,
    idempotency_cache: DashMap<String, CoreAuditEntry>,
}

impl TamperEvidentAuditLedger {
    pub fn new() -> Self {
        Self {
            chain: Mutex::new(Vec::new()),
            idempotency_cache: DashMap::new(),
        }
    }

    pub fn append_sealed_entry(
        &self,
        idempotency_key: &str,
        project_id: u32,
        tenant_id: &str,
        payload_summary: &str,
    ) -> CoreAuditEntry {
        if let Some(existing) = self.idempotency_cache.get(idempotency_key) {
            return existing.clone();
        }

        let mut guard = self.chain.lock().unwrap();
        let seq = (guard.len() as u64) + 1;
        let prev_hash = guard
            .last()
            .map(|e| e.blake3_seal.clone())
            .unwrap_or_else(|| GENESIS_HASH.to_string());

        let record_id = Uuid::new_v4();
        let canonical = format!(
            "{}:{}:{}:{}:{}:{}",
            seq, record_id, project_id, tenant_id, payload_summary, prev_hash
        );
        let blake3_seal = blake3::hash(canonical.as_bytes()).to_hex().to_string();

        let entry = CoreAuditEntry {
            record_id,
            sequence_no: seq,
            project_id,
            tenant_id: tenant_id.to_string(),
            payload_summary: payload_summary.to_string(),
            previous_hash: prev_hash,
            blake3_seal,
            timestamp: Utc::now(),
        };

        guard.push(entry.clone());
        self.idempotency_cache
            .insert(idempotency_key.to_string(), entry.clone());
        entry
    }

    pub fn verify_entire_chain(&self) -> ChainVerificationReport {
        let guard = self.chain.lock().unwrap();
        let mut expected_prev = GENESIS_HASH.to_string();

        for entry in guard.iter() {
            if entry.previous_hash != expected_prev {
                return ChainVerificationReport {
                    total_entries_verified: guard.len(),
                    chain_intact: false,
                    head_blake3_seal: expected_prev,
                };
            }
            let canonical = format!(
                "{}:{}:{}:{}:{}:{}",
                entry.sequence_no,
                entry.record_id,
                entry.project_id,
                entry.tenant_id,
                entry.payload_summary,
                entry.previous_hash
            );
            let computed = blake3::hash(canonical.as_bytes()).to_hex().to_string();
            if computed != entry.blake3_seal {
                return ChainVerificationReport {
                    total_entries_verified: guard.len(),
                    chain_intact: false,
                    head_blake3_seal: expected_prev,
                };
            }
            expected_prev = entry.blake3_seal.clone();
        }

        ChainVerificationReport {
            total_entries_verified: guard.len(),
            chain_intact: true,
            head_blake3_seal: expected_prev,
        }
    }
}

impl Default for TamperEvidentAuditLedger {
    fn default() -> Self {
        Self::new()
    }
}


#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct LedgerBlock {
    pub sequence_no: u64,
    pub record_id: uuid::Uuid,
    pub tenant_id: String,
    pub project_id: u32,
    pub output_metric: u64,
    pub previous_hash: String,
    pub blake3_seal: String,
    pub created_at: chrono::DateTime<chrono::Utc>,
}

impl LedgerBlock {
    pub fn create(
        sequence_no: u64,
        tenant_id: String,
        project_id: u32,
        output_metric: u64,
        previous_hash: &str,
    ) -> Self {
        let record_id = uuid::Uuid::new_v4();
        let created_at = chrono::Utc::now();
        let payload = format!("{sequence_no}:{tenant_id}:{project_id}:{output_metric}:{previous_hash}");
        let blake3_seal = blake3::hash(payload.as_bytes()).to_hex().to_string();
        Self {
            sequence_no,
            record_id,
            tenant_id,
            project_id,
            output_metric,
            previous_hash: previous_hash.to_string(),
            blake3_seal,
            created_at,
        }
    }
}
