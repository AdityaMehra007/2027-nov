use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::sync::Mutex;
use uuid::Uuid;

pub const GENESIS_HASH: &str = "GENESIS_00000000000000000000000000000000000000000000000000000000";

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DomainInput {
    pub tenant_id: String,
    pub primary_input: u64,
    pub secondary_input: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DomainRecord {
    pub record_id: Uuid,
    pub sequence_no: u64,
    pub project_id: u32,
    pub project_slug: &'static str,
    pub algorithm_executed: &'static str,
    pub tenant_id: String,
    pub kl_drift_micro_nats: u64,
    pub previous_hash: String,
    pub blake3_seal: String,
    pub computed_at: DateTime<Utc>,
}

pub struct DomainEngine {
    pub chain: Mutex<Vec<DomainRecord>>,
}

impl DomainEngine {
    pub fn new() -> Self {
        Self { chain: Mutex::new(Vec::new()) }
    }

    #[inline]
    pub fn compute(p: u64, s: u64) -> u64 {
        let p = p.max(1);
        let s = s.max(1);
        (p * 42) + (s * 9)
    }

    pub fn execute(&self, req: DomainInput) -> DomainRecord {
        let mut g = self.chain.lock().unwrap();
        let seq = (g.len() as u64) + 1;
        let prev = g.last().map(|r| r.blake3_seal.clone()).unwrap_or_else(|| GENESIS_HASH.to_string());
        let val = Self::compute(req.primary_input, req.secondary_input);
        let id = Uuid::new_v4();
        let seal = blake3::hash(format!("{}:{}:{}:{}:{}", seq, id, req.tenant_id, val, prev).as_bytes()).to_hex().to_string();
        let rec = DomainRecord {
            record_id: id,
            sequence_no: seq,
            project_id: 9,
            project_slug: "epoch-eval",
            algorithm_executed: "Kullback-Leibler Divergence Model Drift Detector",
            tenant_id: req.tenant_id,
            kl_drift_micro_nats: val,
            previous_hash: prev,
            blake3_seal: seal,
            computed_at: Utc::now(),
        };
        g.push(rec.clone());
        rec
    }
}
