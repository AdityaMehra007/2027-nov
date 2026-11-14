"""
ATLAS NEXUS: Department & Capability Matrix
Defines the 9 Institutional Departments and 50 Frontier Capabilities.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class DepartmentEnum(str, Enum):
    DEPT_A = "Universal Intelligence"
    DEPT_B = "Science and Frontier Technology"
    DEPT_C = "Computational and Engineering Systems"
    DEPT_D = "Business and Economic Intelligence"
    DEPT_E = "Human Knowledge and Education"
    DEPT_F = "World and Infrastructure"
    DEPT_G = "Creation and Execution"
    DEPT_H = "Control and Governance"
    DEPT_I = "Advanced Intelligence"


@dataclass(frozen=True)
class CapabilityDescriptor:
    id: int
    name: str
    department: DepartmentEnum
    description: str
    engine_target: Optional[str] = None


CAPABILITY_DEFINITIONS: List[CapabilityDescriptor] = [
    # Department A: Universal Intelligence (1-5)
    CapabilityDescriptor(1, "Universal Intelligence Engine", DepartmentEnum.DEPT_A, "Multi-domain query reasoning, cross-field synthesis, and unified intent routing.", "CursorASTSemanticEngine"),
    CapabilityDescriptor(2, "Research Intelligence", DepartmentEnum.DEPT_A, "Scholarly source ingestion, citation extraction, and literature review synthesis.", "LinUCB"),
    CapabilityDescriptor(3, "Knowledge Graph", DepartmentEnum.DEPT_A, "Entity-relationship ontology, conceptual graphs, and causal dependency tracking.", "MerkleTree"),
    CapabilityDescriptor(4, "Memory Infrastructure", DepartmentEnum.DEPT_A, "Multi-tiered session, episodic, and institutional semantic memory stores.", "ConsistentHashRing"),
    CapabilityDescriptor(5, "Information Verification", DepartmentEnum.DEPT_A, "Claim validation, mathematical proof verification, and hallucination scoring.", "ContinuousLyapunovVerifierEngine"),

    # Department B: Science and Frontier Technology (6-15)
    CapabilityDescriptor(6, "Artificial Intelligence Observatory", DepartmentEnum.DEPT_B, "Tracking model frontiers, benchmarks, capabilities, and algorithmic leaps.", "MicroAutogradTrainer"),
    CapabilityDescriptor(7, "Robotics Intelligence", DepartmentEnum.DEPT_B, "Kinematics, inverse dynamics, trajectory planning, and actuator simulation.", "BioMolecularAndNeuromorphicEngine"),
    CapabilityDescriptor(8, "Quantum Intelligence", DepartmentEnum.DEPT_B, "Quantum error correction, surface codes, and unitary gate simulation.", "SurfaceCodeQuantumEngine"),
    CapabilityDescriptor(9, "Biotechnology Intelligence", DepartmentEnum.DEPT_B, "Protein structure modeling, genomic sequence parsing, and molecular dynamics.", "BioMolecularAndNeuromorphicEngine"),
    CapabilityDescriptor(10, "Materials Intelligence", DepartmentEnum.DEPT_B, "Crystalline structure lattice analysis and material property discovery.", "UniversalBytecodeCompilerAndVM"),
    CapabilityDescriptor(11, "Energy Intelligence", DepartmentEnum.DEPT_B, "Fusion plasma MHD simulation, grid load balancing, and renewables forecasting.", "FourierMhdRk4"),
    CapabilityDescriptor(12, "Space Intelligence", DepartmentEnum.DEPT_B, "Relativistic orbital mechanics, CR3BP trajectory design, and cislunar logistics.", "CislunarCR3BPEngine"),
    CapabilityDescriptor(13, "Climate Intelligence", DepartmentEnum.DEPT_B, "Atmospheric fluid dynamics, carbon cycle modeling, and planetary weather.", "NumPyMhdPinn"),
    CapabilityDescriptor(14, "Medical Research Intelligence", DepartmentEnum.DEPT_B, "Clinical trial synthesis, pharmacological interaction trees, and pathology.", "DisjointLinUCBEngine"),
    CapabilityDescriptor(15, "Scientific Discovery Workspace", DepartmentEnum.DEPT_B, "Automated hypothesis generator and experimental design workflow.", "SymbolicRegressionAIPhysicist"),

    # Department C: Computational and Engineering Systems (16-20)
    CapabilityDescriptor(16, "Simulation Engine", DepartmentEnum.DEPT_C, "Multi-physics numerical integration (Runge-Kutta, Symplectic, PINN).", "NumPyMhdPinn"),
    CapabilityDescriptor(17, "Digital Twin Studio", DepartmentEnum.DEPT_C, "Real-time state synchronization of complex physical and logical systems.", "ConsistentHashRing"),
    CapabilityDescriptor(18, "Software Factory", DepartmentEnum.DEPT_C, "Autonomous multi-file software synthesis, refactoring, and test harness generation.", "UniversalBytecodeCompilerAndVM"),
    CapabilityDescriptor(19, "Hardware and IoT Studio", DepartmentEnum.DEPT_C, "Verilog/VHDL RTL logic synthesis, register transfer simulation, and pinouts.", "UniversalBytecodeCompilerAndVM"),
    CapabilityDescriptor(20, "Data Engineering Studio", DepartmentEnum.DEPT_C, "ETL pipeline orchestration, streaming Kafka/WAL logs, and schema migration.", "ApexLSMDatabase"),

    # Department D: Business and Economic Intelligence (21-25)
    CapabilityDescriptor(21, "Global Economy Engine", DepartmentEnum.DEPT_D, "Macroeconomic trade flow simulations, monetary policy, and interest models.", "DoubleEntryLedger"),
    CapabilityDescriptor(22, "Financial Intelligence", DepartmentEnum.DEPT_D, "High-frequency limit order books, portfolio optimization, and risk engines.", "L3LimitOrderBook"),
    CapabilityDescriptor(23, "Business Operating System", DepartmentEnum.DEPT_D, "Multi-division corporate governance, payroll, ledger reconciliation, and KPIs.", "DoubleEntryLedger"),
    CapabilityDescriptor(24, "Startup Foundry", DepartmentEnum.DEPT_D, "Automated ICP generation, go-to-market playbooks, and unit economics validation.", "VCGMechanismDesign"),
    CapabilityDescriptor(25, "Market and Industry Intelligence", DepartmentEnum.DEPT_D, "Competitive intelligence analysis, TAM sizing, and moat evaluation.", "DisjointLinUCBEngine"),

    # Department E: Human Knowledge and Education (26-30)
    CapabilityDescriptor(26, "Education Operating System", DepartmentEnum.DEPT_E, "Adaptive pedagogical curricula, Socratic tutoring, and mastery graphs.", "CursorASTSemanticEngine"),
    CapabilityDescriptor(27, "Career Intelligence", DepartmentEnum.DEPT_E, "Skill graph projection, career roadmap synthesis, and interview simulation.", "DisjointLinUCBEngine"),
    CapabilityDescriptor(28, "Creativity and Media Studio", DepartmentEnum.DEPT_E, "Generative narrative, technical copywriting, and audio-visual scripting.", "UniversalBytecodeCompilerAndVM"),
    CapabilityDescriptor(29, "Personal Productivity Infrastructure", DepartmentEnum.DEPT_E, "Cognitive load optimization, focus telemetry, and task graph sequencing.", "CursorASTSemanticEngine"),
    CapabilityDescriptor(30, "Collaborative Knowledge Workspace", DepartmentEnum.DEPT_E, "Multiplayer conflict-free replicated editing (CRDT) and collaborative wikis.", "ConsistentHashRing"),

    # Department F: World and Infrastructure (31-35)
    CapabilityDescriptor(31, "Global Geography Intelligence", DepartmentEnum.DEPT_F, "Geopolitical boundary mapping, infrastructure graphs, and trade corridors.", "CislunarCR3BPEngine"),
    CapabilityDescriptor(32, "Urban Intelligence", DepartmentEnum.DEPT_F, "Smart city traffic flow, municipal utility routing, and zoning simulation.", "NumPyMhdPinn"),
    CapabilityDescriptor(33, "Agriculture and Food Intelligence", DepartmentEnum.DEPT_F, "Soil moisture forecasting, crop yield modeling, and supply distribution.", "FourierMhdRk4"),
    CapabilityDescriptor(34, "Supply Chain Intelligence", DepartmentEnum.DEPT_F, "Global freight network flow, bottleneck mitigation, and inventory buffers.", "DoubleEntryLedger"),
    CapabilityDescriptor(35, "Geospatial Intelligence", DepartmentEnum.DEPT_F, "Satellite telemetry, SAR signal processing, and terrain elevation mapping.", "FLRWCosmologicalIntegrator"),

    # Department G: Creation and Execution (36-40)
    CapabilityDescriptor(36, "Product Foundry", DepartmentEnum.DEPT_G, "End-to-end product specification, MVP wireframing, and tracer-bullet scaffolding.", "UniversalBytecodeCompilerAndVM"),
    CapabilityDescriptor(37, "Agent Foundry", DepartmentEnum.DEPT_G, "Multi-agent persona synthesis, tool binding, and role prompt engineering.", "CursorASTSemanticEngine"),
    CapabilityDescriptor(38, "Workflow Automation", DepartmentEnum.DEPT_G, "Deterministic state machine execution, webhook routing, and cron pipelines.", "ApexLSMDatabase"),
    CapabilityDescriptor(39, "API and Integration Marketplace", DepartmentEnum.DEPT_G, "OpenAPI schema generation, webhook validation, and third-party connector adapters.", "AuroraQuorumCluster"),
    CapabilityDescriptor(40, "Application Generation", DepartmentEnum.DEPT_G, "Full-stack web/mobile application code generation with tests and deployment configs.", "UniversalBytecodeCompilerAndVM"),

    # Department H: Control and Governance (41-45)
    CapabilityDescriptor(41, "Cybersecurity", DepartmentEnum.DEPT_H, "STRIDE threat modeling, static analysis vulnerability auditing, and sanitization.", "AuroraQuorumCluster"),
    CapabilityDescriptor(42, "Identity and Access Management", DepartmentEnum.DEPT_H, "Role-based access control, cryptographic key pairs, and post-quantum auth.", "PostQuantumLWE"),
    CapabilityDescriptor(43, "AI Governance", DepartmentEnum.DEPT_H, "Safety boundaries, compute budget throttling, and ethical constraint validation.", "ContinuousLyapunovVerifierEngine"),
    CapabilityDescriptor(44, "Cost and Compute Management", DepartmentEnum.DEPT_H, "Token accounting, GPU quota scheduling, and cost-per-inference metrics.", "DoubleEntryLedger"),
    CapabilityDescriptor(45, "Observability", DepartmentEnum.DEPT_H, "OpenTelemetry-style distributed tracing, audit logging, and health heartbeats.", "ApexLSMDatabase"),

    # Department I: Advanced Intelligence (46-50)
    CapabilityDescriptor(46, "Research Gap Discovery", DepartmentEnum.DEPT_I, "Automated identification of unproven theorems and unbuilt engineering systems.", "AutomatedTheoremProverDPLL"),
    CapabilityDescriptor(47, "Patent and Prior-Art Explorer", DepartmentEnum.DEPT_I, "Novelty scoring, claim breadth analysis, and patent infringement auditing.", "SymbolicRegressionAIPhysicist"),
    CapabilityDescriptor(48, "Future Scenario Laboratory", DepartmentEnum.DEPT_I, "Monte Carlo socio-technical projection and civilizational tail-risk simulation.", "MatrioshkaBrain2075"),
    CapabilityDescriptor(49, "Autonomous Evaluation System", DepartmentEnum.DEPT_I, "Multi-model adversarial evaluation, red teaming, and regression benchmarking.", "AutomatedTheoremProverDPLL"),
    CapabilityDescriptor(50, "Impact Observatory", DepartmentEnum.DEPT_I, "Planetary ecological and economic net impact quantification.", "BekensteinHawkingUltimateComputer2126"),
]


class CapabilityRegistry:
    def __init__(self) -> None:
        self._capabilities: Dict[int, CapabilityDescriptor] = {
            c.id: c for c in CAPABILITY_DEFINITIONS
        }

    def get_all(self) -> List[CapabilityDescriptor]:
        return list(self._capabilities.values())

    def get_by_id(self, cap_id: int) -> Optional[CapabilityDescriptor]:
        return self._capabilities.get(cap_id)

    def filter_by_department(self, dept: DepartmentEnum) -> List[CapabilityDescriptor]:
        return [c for c in self._capabilities.values() if c.department == dept]


_GLOBAL_REGISTRY = CapabilityRegistry()


def get_all_capabilities() -> List[CapabilityDescriptor]:
    return _GLOBAL_REGISTRY.get_all()


def get_capability_by_id(cap_id: int) -> Optional[CapabilityDescriptor]:
    return _GLOBAL_REGISTRY.get_by_id(cap_id)
