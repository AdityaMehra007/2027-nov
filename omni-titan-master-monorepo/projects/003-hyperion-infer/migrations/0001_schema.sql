CREATE TABLE IF NOT EXISTS omni_003_hyperion_infer_ledger (
    record_id UUID PRIMARY KEY,
    sequence_no BIGINT NOT NULL UNIQUE,
    tenant_id VARCHAR(128) NOT NULL,
    kv_blocks_allocated BIGINT NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    blake3_seal VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
