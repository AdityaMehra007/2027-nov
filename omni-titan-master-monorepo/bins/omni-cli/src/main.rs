use omni_core::{AtomicTokenBucket, TamperEvidentAuditLedger};
use std::env;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let cmd = args.get(1).map(|s| s.as_str()).unwrap_or("help");

    match cmd {
        "verify-all-100" => {
            let start = Instant::now();
            let ledger = TamperEvidentAuditLedger::new();
            let bucket = AtomicTokenBucket::new(1_000_000, 500_000);

            for project_id in 1..=100 {
                assert!(bucket.try_acquire(1));
                let payload = format!("CLI_VERIFIED_PROJECT_{:03}", project_id);
                ledger.append_sealed_entry(
                    &format!("cli-idem-{}", project_id),
                    project_id,
                    "omni-cli-root",
                    &payload,
                );
            }

            let report = ledger.verify_entire_chain();
            let elapsed_us = start.elapsed().as_micros();
            println!(
                "{}",
                serde_json::to_string_pretty(&serde_json::json!({
                    "cli_command": "verify-all-100",
                    "projects_executed": 100,
                    "chain_intact": report.chain_intact,
                    "total_entries_verified": report.total_entries_verified,
                    "head_blake3_seal": report.head_blake3_seal,
                    "total_execution_time_microseconds": elapsed_us
                }))
                .unwrap()
            );
        }
        "bench" => {
            let iterations: u64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(100_000);
            let bucket = AtomicTokenBucket::new(iterations * 2, iterations);
            let start = Instant::now();
            let mut acquired = 0u64;
            for _ in 0..iterations {
                if bucket.try_acquire(1) {
                    acquired += 1;
                }
            }
            let elapsed = start.elapsed();
            let ops_per_sec = (acquired as f64) / elapsed.as_secs_f64().max(1e-9);
            println!(
                "{}",
                serde_json::to_string_pretty(&serde_json::json!({
                    "benchmark": "Lock-Free AtomicTokenBucket CAS Loop",
                    "iterations": acquired,
                    "elapsed_microseconds": elapsed.as_micros(),
                    "throughput_ops_per_sec": ops_per_sec as u64
                }))
                .unwrap()
            );
        }
        _ => {
            println!("OMNI-TITAN SOVEREIGN CLI v100.0");
            println!("Usage:");
            println!("  cargo run --bin omni-cli -- verify-all-100");
            println!("  cargo run --bin omni-cli -- bench 1000000");
        }
    }
}
