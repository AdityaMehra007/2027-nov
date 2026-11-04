import pytest
from omniverse.modules.planetary_mesh.models import MeshRegion, NodeStatus, TelemetryPacket
from omniverse.modules.planetary_mesh.federation import GlobalPlanetaryMesh

def test_planetary_mesh_federation_initialization():
    mesh = GlobalPlanetaryMesh()
    nodes = mesh.list_nodes()
    
    assert len(nodes) >= 6 # Nodes across continents
    regions = {n.region for n in nodes}
    assert MeshRegion.ASIA_SOUTH in regions
    assert MeshRegion.NORTH_AMERICA in regions
    assert MeshRegion.EUROPE_CENTRAL in regions

def test_planetary_mesh_packet_broadcast():
    mesh = GlobalPlanetaryMesh()
    packet = TelemetryPacket(
        source_node_id="NODE-BLR-01",
        event_type="DISASTER_ALERT",
        payload={"hazard": "FLOOD", "severity": 8.5, "coordinates": [12.9716, 77.5946]}
    )
    result = mesh.broadcast_packet(packet)
    assert result["broadcast_status"] == "DELIVERED"
    assert result["nodes_reached"] >= 5
    assert result["latency_ms"] < 25.0

def test_planetary_mesh_consensus():
    mesh = GlobalPlanetaryMesh()
    consensus = mesh.reach_federated_consensus(proposal_id="PROP-RISK-771", proposed_value=99.07)
    assert consensus["consensus_reached"] is True
    assert consensus["agreement_percentage"] >= 66.7
