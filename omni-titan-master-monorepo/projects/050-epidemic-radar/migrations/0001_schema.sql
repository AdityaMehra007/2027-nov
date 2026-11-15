CREATE TABLE IF NOT EXISTS omni_050_epidemic_radar_ledger (
    record_id UUID PRIMARY KEY,
    sequence_no BIGINT NOT NULL UNIQUE,
    tenant_id VARCHAR(128) NOT NULL,
    sir_r0_milli_units BIGINT NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    blake3_seal VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
