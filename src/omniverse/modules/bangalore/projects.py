"""Bangalore Engineering Archetypes & Flagship Production Systems Catalog."""

from typing import List, Optional
from omniverse.modules.bangalore.models import ProjectArchetype

_PROJECT_ARCHETYPES: List[ProjectArchetype] = [
    ProjectArchetype(
        project_id="BLR-PROJ-01",
        name="Ultra-Low Latency Dark Store Dispatch & Routing Engine",
        primary_sector="Quick-Commerce & Hyperlocal Logistics",
        archetype_companies=["Zepto", "Swiggy Instamart", "Blinkit"],
        architecture_summary="Event-driven distributed inventory allocation, sub-second route dispatch, and rider batching with geo-hashing (H3/S2 cells).",
        core_tech_stack=["Go", "Kafka", "Redis", "PostgreSQL", "Rust"],
        scale_metrics={
            "orders_per_minute": 25000,
            "p99_dispatch_latency_ms": 120.0,
            "delivery_window_minutes": 10.0
        },
        engineering_challenges=[
            "Inventory locking across concurrency spikes during IPL matches",
            "Dynamic SLA re-routing under Silk Board and ORR congestion",
            "Sub-100ms multi-drop batched traveling salesperson optimization"
        ]
    ),
    ProjectArchetype(
        project_id="BLR-PROJ-02",
        name="High-Throughput NPCI UPI Switch & Reconciliation Engine",
        primary_sector="FinTech Payments & Neo-Banking",
        archetype_companies=["PhonePe", "Razorpay", "CRED"],
        architecture_summary="Idempotent, active-active multi-region transactional switch processing 15,000 TPS with automated NPCI reversal resolution.",
        core_tech_stack=["Java", "Spring Boot", "Cassandra", "Kafka", "RocksDB"],
        scale_metrics={
            "peak_tps": 18500,
            "success_rate_percentage": 99.85,
            "daily_volume_inr": 12000000000.0
        },
        engineering_challenges=[
            "Strict zero-double-spend ledger consistency over flaky mobile connections",
            "Handling bank CBS timeouts without dropping user balance state",
            "Real-time fraud scoring under 25ms using sliding window bloom filters"
        ]
    ),
    ProjectArchetype(
        project_id="BLR-PROJ-03",
        name="Global GCC Enterprise Analytics & Regulatory Data Fabric",
        primary_sector="Global Capability Centers (GCC)",
        archetype_companies=["Walmart Global Tech", "Target India", "Goldman Sachs Bengaluru"],
        architecture_summary="Federated lakehouse unified across AWS and Azure with Apache Iceberg, automated GDPR/DPDP data redaction, and sub-minute query response.",
        core_tech_stack=["Python", "Apache Spark", "Iceberg", "Trino", "Terraform"],
        scale_metrics={
            "daily_ingestion_tb": 45.0,
            "query_p95_seconds": 1.8,
            "tenant_clusters": 120
        },
        engineering_challenges=[
            "Cross-border sovereign data governance under India DPDP Act",
            "Petabyte-scale schema evolution without stopping continuous CDC pipelines",
            "Cost optimization across spot instance fleets and cold tier lifecycle policies"
        ]
    ),
    ProjectArchetype(
        project_id="BLR-PROJ-04",
        name="Global Developer Platform & API Observability Mesh",
        primary_sector="DevTools & Cloud Infrastructure SaaS",
        archetype_companies=["Postman", "BrowserStack", "Hasura"],
        architecture_summary="Globally distributed edge proxies with distributed tracing, GraphQL aggregation, and real-time collaborative workspace synchronization.",
        core_tech_stack=["TypeScript", "Rust", "Node.js", "ClickHouse", "Wasm"],
        scale_metrics={
            "active_developers": 35000000,
            "monthly_api_calls_billion": 120.0,
            "global_edge_locations": 48
        },
        engineering_challenges=[
            "CRDT-based conflict-free collaborative document and schema editing",
            "High-cardinality distributed trace indexing with sub-second search",
            "Zero-trust mTLS proxy mesh with automated ephemeral token rotation"
        ]
    ),
    ProjectArchetype(
        project_id="BLR-PROJ-05",
        name="Planetary Earth Observation & Autonomous Satellite Telemetry",
        primary_sector="Deep Tech, Space & Defense",
        archetype_companies=["ISRO", "HAL", "Bellatrix Aerospace", "Pixxel"],
        architecture_summary="Synthetic Aperture Radar (SAR) and hyperspectral imagery processing pipeline with onboard edge AI inference and telemetry downlinks.",
        core_tech_stack=["C++", "Python", "CUDA", "GDAL", "PyTorch"],
        scale_metrics={
            "ground_station_passes_daily": 32,
            "raw_downlink_gbps": 10.0,
            "swath_resolution_meters": 1.25
        },
        engineering_challenges=[
            "Real-time radiometric calibration and Doppler centroid frequency tracking",
            "Radiation-hardened embedded flight software with strict watchdog recovery",
            "Distributed ground station orbit pass scheduling and antenna slew control"
        ]
    )
]

def get_project_archetypes() -> List[ProjectArchetype]:
    """Returns the full catalog of Bangalore flagship engineering project archetypes."""
    return _PROJECT_ARCHETYPES

def get_project_by_id(project_id: str) -> Optional[ProjectArchetype]:
    """Retrieves a specific Bangalore engineering archetype by its identifier."""
    for proj in _PROJECT_ARCHETYPES:
        if proj.project_id == project_id:
            return proj
    return None
