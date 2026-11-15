-- Master Planetary Ledger & Tenant Telemetry Table
CREATE TABLE IF NOT EXISTS omni_master_singularity_ledger (
    sequence_no BIGSERIAL PRIMARY KEY,
    record_id UUID NOT NULL UNIQUE,
    tenant_id VARCHAR(128) NOT NULL,
    project_id INTEGER NOT NULL CHECK (project_id BETWEEN 1 AND 112),
    output_metric BIGINT NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    blake3_seal VARCHAR(64) NOT NULL,
    computed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ledger_tenant ON omni_master_singularity_ledger(tenant_id);
CREATE INDEX IF NOT EXISTS idx_ledger_project ON omni_master_singularity_ledger(project_id);
CREATE INDEX IF NOT EXISTS idx_ledger_seal ON omni_master_singularity_ledger(blake3_seal);
