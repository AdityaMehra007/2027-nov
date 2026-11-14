"""
ATLAS NEXUS: Python SDK Client
Enables both in-process and remote HTTP interaction with ATLAS NEXUS.
"""

from typing import Any, Dict, List, Optional
from src.nexus.command import NexusCommandCenter, ProjectDirective
from src.nexus.departments import (
    CapabilityDescriptor,
    CapabilityRegistry,
    get_all_capabilities,
    get_capability_by_id,
)
from src.nexus.orchestrator import (
    ExecutionManifest,
    OrchestratorTelemetry,
    UniversalOrchestrator,
)


class NexusClient:
    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url
        self._command_center = NexusCommandCenter()
        self._orchestrator = UniversalOrchestrator()

    def submit_directive(
        self,
        raw_input: str,
        user_id: str = "aditya",
        priority: str = "NORMAL",
    ) -> ProjectDirective:
        return self._command_center.parse_intake(
            raw_input=raw_input,
            user_id=user_id,
            priority=priority,
        )

    def execute(
        self,
        raw_input: str,
        user_id: str = "aditya",
        priority: str = "NORMAL",
    ) -> ExecutionManifest:
        directive = self.submit_directive(raw_input=raw_input, user_id=user_id, priority=priority)
        return self._orchestrator.dispatch(directive)

    def get_capabilities(self) -> List[CapabilityDescriptor]:
        return self._command_center.list_capabilities()

    def get_capability(self, cap_id: int) -> Optional[CapabilityDescriptor]:
        return self._command_center.get_capability(cap_id)

    def get_telemetry(self) -> OrchestratorTelemetry:
        return self._orchestrator.get_telemetry()
