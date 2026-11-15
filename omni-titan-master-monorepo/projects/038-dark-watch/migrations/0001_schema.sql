CREATE TABLE IF NOT EXISTS omni_038_dark_watch_ledger (
    record_id UUID PRIMARY KEY,
    sequence_no BIGINT NOT NULL UNIQUE,
    tenant_id VARCHAR(128) NOT NULL,
    breached_sessions_revoked BIGINT NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    blake3_seal VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
