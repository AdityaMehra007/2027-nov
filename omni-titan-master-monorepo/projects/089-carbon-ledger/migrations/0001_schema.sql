CREATE TABLE IF NOT EXISTS omni_089_carbon_ledger_ledger (
    record_id UUID PRIMARY KEY,
    sequence_no BIGINT NOT NULL UNIQUE,
    tenant_id VARCHAR(128) NOT NULL,
    scope3_kg_co2e_calculated BIGINT NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    blake3_seal VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
