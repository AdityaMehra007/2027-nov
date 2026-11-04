from typing import List, Optional
from omniverse.modules.bangalore.models import ProjectArchetype

PROJECT_ARCHETYPES: List[ProjectArchetype] = [
    ProjectArchetype(
        project_id="BLR-PROJ-01",
        name="Hyperlocal Real-Time Quick-Commerce Dispatch & Dark Store Engine",
        primary_sector="Quick-Commerce & Hyperlocal Logistics",
        archetype_companies=["Zepto", "Swiggy Instamart", "Blinkit"],
        architecture_summary=(
            "Distributed event-driven geospatial dispatch fabric. Ingests customer orders, "
            "evaluates dark store inventory locks within 50ms, groups orders into multi-drop routes "
            "using Uber H3 spatial indexing, and tracks riders in real-time."
        ),
        core_tech_stack=["Go", "Kafka", "H3 Spatial Hex Index", "Redis Cluster", "PostgreSQL", "Rust"],
        scale_metrics={
            "daily_order_volume": 1500000,
            "dispatch_p99_latency_ms": 22,
            "delivery_sla_minutes": 10,
            "peak_tps": 12000,
        },
        engineering_challenges=[
            "Silk Board & ORR traffic choke-point avoidance via dynamic telemetry",
            "Distributed microsecond inventory locking during flash demand surges",
            "Dynamic rider batching under heavy monsoon rain downpours",
        ],
    ),
    ProjectArchetype(
        project_id="BLR-PROJ-02",
        name="Sub-10ms High-Concurrency NPCI UPI Switch & Dual-Ledger Gateway",
        primary_sector="FinTech & Payment Infrastructure",
        archetype_companies=["Razorpay", "PhonePe", "CRED", "Juspay"],
        architecture_summary=(
            "Mission-critical transaction switch communicating directly with NPCI UPI networks and "
            "sponsor bank remitter/beneficiary systems. Employs distributed state-machine saga patterns "
            "to guarantee zero-loss idempotent payment reconciliation."
        ),
        core_tech_stack=["Java 21", "Spring Boot", "Apache Kafka", "ScyllaDB", "Redis", "Envoy"],
        scale_metrics={
            "peak_tps": 32000,
            "switch_p99_latency_ms": 8,
            "availability_sla": "99.999%",
            "annual_tpv_inr": 8500000000000.0,
        },
        engineering_challenges=[
            "Handling unpredictable sponsor bank core-banking system downtime spikes",
            "Cryptographic signature verification on millions of UPI intent requests",
            "Double-spend prevention across distributed network partitions",
        ],
    ),
    ProjectArchetype(
        project_id="BLR-PROJ-03",
        name="Enterprise Multi-Tenant Planetary Data Lake & ML Feature Store",
        primary_sector="GCC Enterprise Tech Platforms",
        archetype_companies=["Walmart Global Tech", "Goldman Sachs", "Target Tech Center", "Grab"],
        architecture_summary=(
            "Centralized data lakehouse consolidating telemetry, transactional records, and supply "
            "chain data across global retail and financial subsidiaries. Delivers real-time feature "
            "pipelines for ML fraud scoring and inventory forecasting."
        ),
        core_tech_stack=["Apache Spark", "Apache Iceberg", "Snowflake", "Trino", "Python", "Kubernetes", "Ray"],
        scale_metrics={
            "storage_petabytes": 45,
            "daily_queries": 120000,
            "feature_serving_latency_ms": 15,
            "global_tenants": 240,
        },
        engineering_challenges=[
            "Cross-border data sovereignty compliance under Indian DPDP and EU GDPR",
            "Automated schema evolution without disrupting 500+ downstream pipelines",
            "Cost optimization across multi-cloud GPU training clusters",
        ],
    ),
    ProjectArchetype(
        project_id="BLR-PROJ-04",
        name="Collaborative Developer API Platform & Microservices Gateway",
        primary_sector="Developer Tooling & B2B SaaS",
        archetype_companies=["Postman", "Hasura", "BrowserStack"],
        architecture_summary=(
            "Global distributed developer platform supporting real-time collaborative API testing, "
            "instant GraphQL generation over legacy databases, and distributed device cloud testing."
        ),
        core_tech_stack=["TypeScript", "Node.js", "GraphQL", "Rust", "Docker", "WebSockets", "ClickHouse"],
        scale_metrics={
            "registered_developers": 30000000,
            "daily_api_mock_calls": 850000000,
            "active_workspaces": 4500000,
        },
        engineering_challenges=[
            "Multi-region state synchronization with conflict-free replicated data types (CRDTs)",
            "Managing hundreds of thousands of concurrent WebSocket connections",
            "Ultra-fast sandbox isolation for arbitrary developer test scripts",
        ],
    ),
    ProjectArchetype(
        project_id="BLR-PROJ-05",
        name="Aerospace Satellite Telemetry & Mission Control Avionics Fabric",
        primary_sector="Deep Tech & Space Defense Systems",
        archetype_companies=["ISRO", "HAL", "BEL", "Pixxel"],
        architecture_summary=(
            "Hard real-time deterministic command and control system managing low-earth orbit (LEO) "
            "satellite constellation telemetry, payload data downlinks, and avionics flight computers."
        ),
        core_tech_stack=["C++20", "Rust", "RTOS", "ZeroMQ", "Python", "WebAssembly", "InfluxDB"],
        scale_metrics={
            "telemetry_sample_rate_hz": 10000,
            "flight_loop_latency_us": 250,
            "sensor_channels": 4096,
        },
        engineering_challenges=[
            "Strict zero-heap memory allocation guarantees inside embedded flight loops",
            "Byzantine sensor fault tolerance during high-radiation solar storm events",
            "Real-time synthetic aperture radar (SAR) edge processing on orbital compute",
        ],
    ),
]


def get_project_archetypes() -> List[ProjectArchetype]:
    """Returns the comprehensive directory of top Bengaluru engineering project archetypes."""
    return PROJECT_ARCHETYPES


def get_project_by_id(project_id: str) -> Optional[ProjectArchetype]:
    """Finds an engineering project archetype by unique ID."""
    for project in PROJECT_ARCHETYPES:
        if project.project_id.upper() == project_id.upper():
            return project
    return None
