# OmniSwarm Peer Mesh & Supervised Actor Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify OmniSwarm Phase 1: a decentralized, peer-to-peer autonomous agent mesh with Ed25519 cryptographic identity, priority-queued actor mailboxes, Erlang-style self-healing supervision trees, SWIM epidemic gossip membership protocol, and duplex WebSocket transport.

**Architecture:** A dedicated `omniverse.swarm` subsystem interfacing with Omniverse `SecurityGovernor` and `EventBus`. The system provides deterministic signed messaging, bounded priority queues, automatic failure detection and refutation, and an integrated CLI.

**Tech Stack:** Python 3.11+, `cryptography.hazmat.primitives.asymmetric.ed25519`, `asyncio`, `pydantic` v2, `starlette`/`fastapi` WebSockets, `pytest`, `pytest-asyncio`.

**Spec:** `docs/superpowers/specs/2026-11-04-omniswarm-mesh-design.md`

## Global Constraints
- Python 3.11+ compatibility.
- Zero external daemons (no Redis, no Erlang VM, no Consul); pure async Python with standard cryptography.
- Air-gapped compliance: Privileged actions must check `SecurityGovernor.check_action(...)`.
- Test coverage: Every module must have complete unit test coverage with all existing 116 tests remaining green.
- Performance target: Local actor dispatch latency < 2ms, throughput > 10,000 msg/sec.

---

### Task 1: Cryptographic Identity & Wire Envelope Models

**Files:**
- Create: `src/omniverse/swarm/models.py`
- Create: `src/omniverse/swarm/crypto.py`
- Test: `tests/test_swarm_crypto.py`

**Interfaces:**
- Produces:
  - `MessagePriority(IntEnum)`: `EMERGENCY=0`, `HIGH=1`, `NORMAL=2`, `LOW=3`
  - `ActorState(str, Enum)`: `STARTING`, `ACTIVE`, `BUSY`, `SUSPENDED`, `FAILED`, `TERMINATED`
  - `SwarmMessage(BaseModel)`: Envelope with message_id, sender_node_id, sender_actor_id, recipient_node_id, recipient_actor_id, channel, priority, timestamp, nonce, payload, signature
  - `PeerNode(BaseModel)`: node_id, host, port, status (`alive`, `suspect`, `dead`), incarnation, last_seen
  - `SwarmCrypto`:
    - `generate_keypair() -> tuple[ed25519.Ed25519PrivateKey, ed25519.Ed25519PublicKey]`
    - `derive_node_id(public_key: ed25519.Ed25519PublicKey) -> str`
    - `sign_message(private_key: ed25519.Ed25519PrivateKey, envelope_dict: dict) -> str`
    - `verify_signature(public_key: ed25519.Ed25519PublicKey, envelope_dict: dict, signature_hex: str) -> bool`

- [ ] **Step 1: Write the failing tests for models & crypto**
- [ ] **Step 2: Run test to verify it fails** (`pytest tests/test_swarm_crypto.py -v`)
- [ ] **Step 3: Implement `models.py` and `crypto.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit** (`git commit -m "feat(swarm): add models and Ed25519 cryptographic identity"`)

---

### Task 2: Prioritized Actor Mailbox & Dead Letter Queue (DLQ)

**Files:**
- Create: `src/omniverse/swarm/mailbox.py`
- Test: `tests/test_swarm_mailbox.py`

**Interfaces:**
- Consumes: `SwarmMessage`, `MessagePriority` from `src/omniverse/swarm/models.py`
- Produces:
  - `MailboxFullError(Exception)`
  - `DeadLetterQueue`: Class storing quarantined messages with failure reason and timestamp.
  - `ActorMailbox`:
    - `__init__(capacity: int = 1000)`
    - `async push(message: SwarmMessage) -> None`: Inserts into `asyncio.PriorityQueue` by priority rank and sequence id.
    - `async pop() -> SwarmMessage`: Dequeues highest priority message.
    - `size() -> int`
    - `is_empty() -> bool`
    - `quarantine(message: SwarmMessage, reason: str) -> None`: Pushes to DLQ.

- [ ] **Step 1: Write failing tests for priority queue ordering and DLQ**
- [ ] **Step 2: Run test to verify it fails** (`pytest tests/test_swarm_mailbox.py -v`)
- [ ] **Step 3: Implement `ActorMailbox` and `DeadLetterQueue`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit** (`git commit -m "feat(swarm): implement prioritized actor mailbox and dead letter queue"`)

---

### Task 3: Supervised Virtual Actor Kernel & Auto-Healing

**Files:**
- Create: `src/omniverse/swarm/actor.py`
- Test: `tests/test_swarm_actor.py`

**Interfaces:**
- Consumes: `SwarmMessage`, `ActorState` from `models.py`, `ActorMailbox` from `mailbox.py`
- Produces:
  - `RestartPolicy(Enum)`: `ONE_FOR_ONE`, `ALL_FOR_ONE`
  - `SwarmActor`: Base class with `actor_id`, `state`, `receive(msg: SwarmMessage) -> Any`, `start()`, `stop()`.
  - `ActorSupervisor`: Supervises one or more actors, catches crashes, applies backoff retries (max 5 in 60s), maintains mailbox continuity, handles escalation.

- [ ] **Step 1: Write failing tests for SwarmActor lifecycle and ActorSupervisor recovery**
- [ ] **Step 2: Run test to verify it fails** (`pytest tests/test_swarm_actor.py -v`)
- [ ] **Step 3: Implement `SwarmActor` and `ActorSupervisor`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit** (`git commit -m "feat(swarm): implement supervised virtual actor engine with auto-healing"`)

---

### Task 4: SWIM Epidemic Gossip Membership Protocol

**Files:**
- Create: `src/omniverse/swarm/gossip.py`
- Test: `tests/test_swarm_gossip.py`

**Interfaces:**
- Consumes: `PeerNode`, `SwarmMessage` from `models.py`
- Produces:
  - `SWIMGossip`:
    - `__init__(local_node: PeerNode, ping_period: float = 1.0, ping_timeout: float = 0.5, suspect_timeout: float = 5.0)`
    - `add_peer(peer: PeerNode) -> None`
    - `get_active_peers() -> list[PeerNode]`
    - `process_ping(sender: PeerNode) -> dict`
    - `process_ack(sender: PeerNode) -> None`
    - `process_suspect(target_node_id: str, incarnation: int) -> None`
    - `process_alive(target_node: PeerNode) -> None`
    - `tick() -> list[tuple[str, str, dict]]`: Executes probe cycle, returning direct or indirect pings to transmit.

- [ ] **Step 1: Write failing tests for SWIM gossip state transitions and indirect ping-req**
- [ ] **Step 2: Run test to verify it fails** (`pytest tests/test_swarm_gossip.py -v`)
- [ ] **Step 3: Implement `SWIMGossip`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit** (`git commit -m "feat(swarm): implement SWIM epidemic gossip membership protocol"`)

---

### Task 5: Duplex WebSocket Mesh Transport Layer

**Files:**
- Create: `src/omniverse/swarm/transport.py`
- Test: `tests/test_swarm_transport.py`

**Interfaces:**
- Consumes: `SwarmMessage` from `models.py`, `SwarmCrypto` from `crypto.py`
- Produces:
  - `MeshTransport`:
    - `__init__(local_node_id: str, host: str, port: int)`
    - `async start_server() -> None`
    - `async stop() -> None`
    - `async connect_to_peer(peer_node_id: str, url: str) -> bool`
    - `async send_frame(target_node_id: str, message: SwarmMessage) -> bool`
    - `register_inbound_handler(handler_callback)`

- [ ] **Step 1: Write failing tests for duplex WebSocket connection and frame exchange**
- [ ] **Step 2: Run test to verify it fails** (`pytest tests/test_swarm_transport.py -v`)
- [ ] **Step 3: Implement `MeshTransport` using async WebSockets**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit** (`git commit -m "feat(swarm): implement duplex WebSocket mesh transport"`)

---

### Task 6: Master SwarmKernel, Security Governor Gating & Telemetry

**Files:**
- Create: `src/omniverse/swarm/kernel.py`
- Create: `src/omniverse/swarm/__init__.py`
- Test: `tests/test_swarm_kernel.py`

**Interfaces:**
- Consumes: All `omniverse.swarm.*` components, `SecurityGovernor` from `omniverse.core.security`, `EventBus` from `omniverse.core.event_bus`.
- Produces:
  - `SwarmKernel`:
    - Singleton runtime orchestrating local actors, gossip membership, and mesh transport.
    - `async spawn_actor(actor_class, actor_id, **kwargs) -> SwarmActor`
    - `async send(sender_actor_id: str, recipient_node_id: str, recipient_actor_id: str, channel: str, payload: dict, priority: MessagePriority = MessagePriority.NORMAL) -> str`
    - `async broadcast(sender_actor_id: str, channel: str, payload: dict) -> None`
    - `async start() -> None`, `async shutdown() -> None`

- [ ] **Step 1: Write failing tests for SwarmKernel routing, governor gating, and EventBus telemetry**
- [ ] **Step 2: Run test to verify it fails** (`pytest tests/test_swarm_kernel.py -v`)
- [ ] **Step 3: Implement `SwarmKernel`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit** (`git commit -m "feat(swarm): implement master SwarmKernel with security governance"`)

---

### Task 7: CLI Management & Empirical Benchmarking Suite

**Files:**
- Create: `src/omniverse/swarm/cli.py`
- Modify: `src/omniverse/cli.py`
- Modify: `src/omniverse/operations/benchmark.py`
- Test: `tests/test_swarm_cli.py`

**Interfaces:**
- CLI Commands:
  - `omniverse swarm status`: Outputs active actors, mailbox queues, peer nodes, and health diagnostics.
  - `omniverse swarm benchmark`: Evaluates actor dispatch throughput and signature verification speeds.
  - `omniverse swarm start --port <P>`: Launches standalone swarm node daemon.

- [ ] **Step 1: Write failing tests for CLI subcommands**
- [ ] **Step 2: Run test to verify it fails** (`pytest tests/test_swarm_cli.py -v`)
- [ ] **Step 3: Implement CLI commands and benchmark runner**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit** (`git commit -m "feat(swarm): add CLI management commands and benchmark integration"`)

---

### Task 8: End-to-End Stress Test, Global Verification & Documentation

**Files:**
- Test: `tests/test_swarm_e2e.py`
- Modify: `README.md`
- Modify: `docs/architecture/` or expansion docs

- [ ] **Step 1: Write and run end-to-end stress test with 100 concurrent actors and 10,000 messages**
- [ ] **Step 2: Run full regression test suite (`pytest`) to ensure 100% green tests**
- [ ] **Step 3: Execute CLI commands (`omniverse swarm status`, `omniverse swarm benchmark`)**
- [ ] **Step 4: Update README and documentation**
- [ ] **Step 5: Commit** (`git commit -m "docs(swarm): update README and architectural documentation for OmniSwarm"`)
