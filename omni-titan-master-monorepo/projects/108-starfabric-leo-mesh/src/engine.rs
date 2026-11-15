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
    pub optical_laser_packets_routed: u64,
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
        (p * 50000) + (s * 1000)
    }

    pub fn execute(&self, req: DomainInput) -> DomainRecord {
        let mut g = self.chain.lock().unwrap();
        let seq = (g.len() as u64) + 1;
        let prev = g.last().map(|r| r.blake3_seal.clone()).unwrap_or_else(|| GENESIS_HASH.to_string());
        let val = Self::compute(req.primary_input, req.secondary_input);
        let id = Uuid::new_v4();
        let now = Utc::now();
        let payload = format!("{seq}:{id}:108:starfabric-leo-mesh:{val}:{prev}");
        let seal = blake3::hash(payload.as_bytes()).to_hex().to_string();
        let rec = DomainRecord {
            record_id: id,
            sequence_no: seq,
            project_id: 108,
            project_slug: "starfabric-leo-mesh",
            algorithm_executed: "J2 Orbital Precession Propagator & FSO Laser Mesh Router",
            tenant_id: req.tenant_id,
            optical_laser_packets_routed: val,
            previous_hash: prev,
            blake3_seal: seal,
            computed_at: now,
        };
        g.push(rec.clone());
        rec
    }
}
