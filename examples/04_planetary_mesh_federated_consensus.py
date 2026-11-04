#!/usr/bin/env python3
"""Example 04: Planetary Edge Mesh & Federated Consensus Protocol.

Demonstrates low-latency telemetry routing across 6 continents and
Byzantine fault-tolerant federated quorum agreement.
"""

import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from omniverse.modules.planetary_mesh import GlobalPlanetaryMesh, TelemetryPacket

def main():
    print("================================================================")
    print("  04. OMNIVERSE GLOBAL PLANETARY MESH (6 CONTINENTS)")
    print("================================================================")

    # 1. Initialize Federated Mesh
    mesh = GlobalPlanetaryMesh()
    nodes = mesh.list_nodes()

    print(f"\n🌐 Step 1: Active Federated Edge Nodes ({len(nodes)} Continents):")
    for n in nodes:
        print(f" • [{n.node_id}] {n.region.value:18} | Latency: {n.latency_ms:4.1f}ms | {n.endpoint}")

    # 2. Broadcast High-Priority Telemetry Packet
    print("\n📡 Step 2: Broadcasting Planetary Telemetry Packet...")
    packet = TelemetryPacket(
        source_node_id="NODE-BLR-01",
        event_type="GEO_CRISIS_EARLY_WARNING",
        payload={
            "sensor": "SENTINEL-2",
            "region": "INDIAN_OCEAN_BASIN",
            "anomaly_type": "RAPID_PRESSURE_DROP",
            "severity": 8.7
        }
    )
    bcast = mesh.broadcast_packet(packet)
    print(f" • Broadcast ID        : {bcast['packet_id']}")
    print(f" • Propagation Status  : {bcast['broadcast_status']}")
    print(f" • Nodes Reached       : {bcast['nodes_reached']} / {len(nodes)}")
    print(f" • Global Mean Latency : {bcast['latency_ms']:.2f} ms")

    # 3. Federated Quorum Consensus
    print("\n🗳️ Step 3: Executing Federated Byzantine Quorum Consensus...")
    consensus = mesh.reach_federated_consensus(
        proposal_id="PROP-PLANETARY-QUORUM-77",
        proposed_value={"action": "INITIATE_RELIEF_GRID", "hazard_level": "CRITICAL"}
    )
    print(f" • Proposal ID         : {consensus['proposal_id']}")
    print(f" • Quorum Verified     : {consensus['quorum_verified']}")
    print(f" • Nodes in Agreement  : {consensus['agreement_percentage']}% ({consensus['total_nodes']} nodes)")
    print(f" • Consensus Decision  : {'ACCEPTED' if consensus['consensus_reached'] else 'REJECTED'}")
    print("================================================================")

if __name__ == "__main__":
    main()
