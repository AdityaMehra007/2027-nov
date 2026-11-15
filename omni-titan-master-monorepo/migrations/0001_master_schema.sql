-- OMNI-TITAN MASTER PRODUCTION POSTGRESQL SCHEMA
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS omni_master_audit_ledger (
    sequence_no BIGSERIAL PRIMARY KEY,
    record_id UUID NOT NULL DEFAULT uuid_generate_v4(),
    project_id INTEGER NOT NULL,
    project_slug VARCHAR(64) NOT NULL,
    algorithm_executed VARCHAR(128) NOT NULL,
    tenant_id VARCHAR(128) NOT NULL,
    primary_input BIGINT NOT NULL,
    secondary_input BIGINT NOT NULL,
    output_metric BIGINT NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    blake3_seal VARCHAR(64) NOT NULL,
    computed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_tenant_proj ON omni_master_audit_ledger(tenant_id, project_id);
CREATE INDEX IF NOT EXISTS idx_audit_seal ON omni_master_audit_ledger(blake3_seal);

CREATE TABLE IF NOT EXISTS omni_tenants (
    tenant_id VARCHAR(128) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    tier VARCHAR(32) NOT NULL DEFAULT 'SOVEREIGN_MAX',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO omni_tenants (tenant_id, company_name, tier)
VALUES ('omni-sovereign', 'OMNI-TITAN GLOBAL SOVEREIGN CORP', 'ENTERPRISE_UNLIMITED')
ON CONFLICT (tenant_id) DO NOTHING;
