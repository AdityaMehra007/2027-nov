use std::sync::atomic::{AtomicU64, Ordering};

pub struct TelemetryRegistry {
    pub requests_total: AtomicU64,
    pub blocks_sealed_total: AtomicU64,
    pub errors_total: AtomicU64,
}

impl TelemetryRegistry {
    pub const fn new() -> Self {
        Self {
            requests_total: AtomicU64::new(0),
            blocks_sealed_total: AtomicU64::new(0),
            errors_total: AtomicU64::new(0),
        }
    }

    pub fn record_request(&self) {
        self.requests_total.fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_block(&self) {
        self.blocks_sealed_total.fetch_add(1, Ordering::Relaxed);
    }
}

pub static GLOBAL_TELEMETRY: TelemetryRegistry = TelemetryRegistry::new();
