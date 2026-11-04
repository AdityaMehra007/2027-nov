from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Any, List
import time
import uuid

class MeshRegion(str, Enum):
    ASIA_SOUTH = "ASIA_SOUTH_BLR"
    ASIA_EAST = "ASIA_EAST_TYO"
    NORTH_AMERICA = "NORTH_AMERICA_VA"
    EUROPE_CENTRAL = "EUROPE_CENTRAL_FRA"
    LATIN_AMERICA = "LATIN_AMERICA_SP"
    AFRICA_SOUTH = "AFRICA_SOUTH_CPT"

class NodeStatus(str, Enum):
    ONLINE = "ONLINE"
    SYNCING = "SYNCING"
    ISOLATED = "ISOLATED"

class MeshNode(BaseModel):
    node_id: str
    region: MeshRegion
    endpoint: str
    status: NodeStatus = Field(default=NodeStatus.ONLINE)
    latency_ms: float = 12.0
    active_peers: int = 5
    last_heartbeat: float = Field(default_factory=time.time)

class TelemetryPacket(BaseModel):
    packet_id: str = Field(default_factory=lambda: f"PKT-{uuid.uuid4().hex[:8].upper()}")
    source_node_id: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: float = Field(default_factory=time.time)
