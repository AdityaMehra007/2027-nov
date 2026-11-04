# OMNISWARM: Decentralized Multi-Agent Peer Mesh & Supervised Actor Kernel — System Design Specification

**Date:** 2026-11-04  
**Author:** Antigravity AI & Founder  
**Status:** Approved for Implementation  
**Project:** CASHFLOW INFINITY: OMNIVERSE — Phase 1: OmniSwarm Peer Mesh & Actor Kernel  
**Target Repository:** `e:\2027 nov`  

---

## 1. Executive Summary & Vision

**OmniSwarm** is the decentralized, peer-to-peer autonomous agent mesh operating layer for **CASHFLOW INFINITY: OMNIVERSE**. It upgrades the platform from a centralized monolithic agent architecture into a distributed, fault-tolerant network of hundreds of concurrent micro-agents capable of negotiating tasks, building micro-SaaS applications, and settling transactions across independent peer nodes.

Phase 1 establishes the foundational networking and concurrency substrate:
1. **Cryptographic Identity**: Ed25519 asymmetric keypairs providing unforgeable node fingerprints, digital signatures on all wire frames, and replay prevention.
2. **Supervised Virtual Actor Kernel**: Lightweight, non-blocking asynchronous actors with prioritized mailboxes, self-healing supervision trees (Erlang/OTP-style auto-restarts), and poison-pill isolation via a Dead Letter Queue (DLQ).
3. **Decentralized Membership via SWIM Gossip**: Epidemic peer discovery, heartbeat ping/ack probes, indirect `ping-req` proxying, and failure suspicion state machines operating without centralized directory servers.
4. **Duplex WebSocket Mesh Transport**: Non-blocking bidirectional streaming between nodes with backpressure flow control and graceful reconnection.
5. **Air-Gapped Security Governance**: Mandatory integration with Omniverse's `SecurityGovernor` to gate privileged operations (financial commitments, code execution, file modifications).
6. **Empirical Benchmarking & CLI**: High-throughput benchmarking (>10,000 local messages/sec) and an operator command-line interface (`omniverse swarm ...`).

---

## 2. OmniSwarm Multi-Phase Roadmap

To prevent uncontrolled complexity and ensure institutional reliability, OmniSwarm is decomposed into four sequential phases:

* **Phase 1 (This Specification)**: OmniSwarm Peer Mesh & Actor Kernel (P2P discovery, gossip membership, actor lifecycles, and cryptographic messaging).
* **Phase 2**: Autonomous Task Auction & Market Negotiation Protocol (Agent-to-agent contract bidding, dynamic work dispatching, escrow bonding, and SLA verification).
* **Phase 3**: Autonomous Micro-SaaS Agent Factory (Sandboxed worker agents that autonomously generate, test, lint, and package micro-SaaS applications).
* **Phase 4**: Distributed PBFT Settlement & Global Treasury Ledger (Byzantine fault-tolerant consensus state machine that validates proof-of-work/proof-of-delivery and settles verified credits into the Omniverse ledger).

---

## 3. Architectural Blueprint & File Layout

The swarm subsystem is housed in a clean, isolated package within `src/omniverse/swarm/`:

```
src/omniverse/swarm/
├── __init__.py           # Package exports (SwarmKernel, SwarmActor, SwarmMessage, etc.)
├── crypto.py             # Ed25519 keypair generation, signing, verification, and address hashing
├── models.py             # Pydantic v2 schemas: SwarmMessage, PeerNode, ActorState, Priority
├── mailbox.py            # Priority-queued async mailbox with bounded capacity & drop policies
├── actor.py              # Base SwarmActor, ActorSupervisor, and exponential backoff policies
├── gossip.py             # SWIM epidemic gossip membership (Alive, Suspect, Dead states)
├── transport.py          # Duplex WebSocket server and client mesh connection pool
├── kernel.py             # Master SwarmKernel coordinator & SecurityGovernor integration
└── cli.py                # Subcommand CLI handlers for `omniverse swarm ...`
```

---

## 4. Cryptographic Identity & Wire Protocol

### 4.1 Node & Agent Identity
- Each peer node and virtual agent generates an `Ed25519` private key using `cryptography.hazmat.primitives.asymmetric.ed25519`.
- Node identifiers follow the format: `node_<hex_fingerprint>`, where the fingerprint is derived from the SHA-256 digest of the public key bytes (truncated to 16 hex chars).
- Agent identifiers follow: `agent_<category>_<hex_fingerprint>`.

### 4.2 Message Envelope (`SwarmMessage`)
All inter-actor and inter-node frames adhere to the deterministic Pydantic schema:

```python
class MessagePriority(IntEnum):
    EMERGENCY = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3

class SwarmMessage(BaseModel):
    message_id: str               # UUIDv4
    sender_node_id: str           # node_<fingerprint>
    sender_actor_id: str          # agent_<id>
    recipient_node_id: str        # node_<fingerprint> or '*' for broadcast
    recipient_actor_id: str       # agent_<id> or '*'
    channel: str                  # e.g., 'system.gossip', 'task.auction', 'direct'
    priority: MessagePriority     # EMERGENCY (0) to LOW (3)
    timestamp: str                # ISO 8601 UTC
    nonce: str                    # Random 16-byte hex
    payload: dict[str, Any]       # Message body
    signature: str                # Ed25519 hex signature of canonical JSON
```

### 4.3 Deterministic Canonical Signing & Verification
- Signatures are calculated across canonical JSON bytes with sorted keys and no unnecessary whitespace (`json.dumps(envelope_data, sort_keys=True, separators=(',', ':'))`).
- Replay prevention: Messages with timestamps drifting more than 30 seconds from local clock or duplicate nonces within a sliding 1,000-entry window are rejected immediately.

---

## 5. Supervised Virtual Actor Kernel

### 5.1 Actor Lifecycle States
Each actor adheres to a deterministic state machine:
- `STARTING`: Actor instance initialized, mailbox allocated.
- `ACTIVE`: Mailbox processing loop active, ready to dequeue messages.
- `BUSY`: Currently executing message handler (`receive(msg)`).
- `SUSPENDED`: Temporarily halted by supervisor during circuit break or network backpressure.
- `FAILED`: Uncaught exception encountered; supervisor evaluating recovery policy.
- `TERMINATED`: Gracefully stopped or retries exhausted; mailbox closed.

### 5.2 Priority Mailbox & Backpressure (`mailbox.py`)
- Backed by an `asyncio.PriorityQueue` storing tuples `(priority, sequence_id, message)`.
- Default capacity: 1,000 messages per mailbox.
- **Backpressure Policy**:
  - `REJECT_BACKPRESSURE`: Rejects newly queued messages when capacity is reached, raising `MailboxFullError` back to sender.
  - Poison-Pill Handling: Messages that repeatedly cause unhandled crashes are moved to the node's **Dead Letter Queue (DLQ)**.

### 5.3 Supervisor Auto-Healing (`actor.py`)
- Supervisors monitor assigned actors with `RestartPolicy.ONE_FOR_ONE`.
- Max restart limit: 5 crashes within 60 seconds.
- Exponential backoff delay: `delay = min(base_delay * (2 ** retry_count), max_delay)`.
- When an actor is restarted, its mailbox queue is preserved, allowing unconsumed valid messages to be processed once healthy.

---

## 6. SWIM Epidemic Gossip Membership Protocol (`gossip.py`)

Nodes maintain a decentralized cluster membership table (`alive`, `suspect`, `dead`) without centralized orchestrators:

1. **Direct Probe**: Every cycle ($T_{\text{period}} = 1.0\text{ s}$), node $A$ selects a random active peer $B$ and sends a direct `PING`.
2. **Indirect Probe (`PING-REQ`)**: If $B$ fails to reply with `ACK` within $T_{\text{timeout}} = 500\text{ ms}$, node $A$ selects $k=3$ random peers and requests they probe $B$ via `PING-REQ(target=B)`.
3. **Suspect Window**: If all indirect pings fail, $B$ is gossiped as `SUSPECT` with a $T_{\text{suspect}} = 5.0\text{ s}$ timeout.
4. **Refutation**: If $B$ is healthy, it broadcasts an `ALIVE` refutation with an incremented incarnation sequence number, overriding the suspicion.
5. **Eviction**: If no refutation arrives before $T_{\text{suspect}}$ expires, $B$ transitions to `DEAD` and its transport connection is dropped.

---

## 7. Duplex WebSocket Mesh Transport (`transport.py`)

1. **Inbound Server**: Non-blocking WebSocket listener at `/ws/swarm` managed via ASGI / Starlette.
2. **Outbound Connection Pool**: Maintained pool of persistent client WebSocket connections to known live peers.
3. **Frame Routing**:
   - Outgoing messages for remote nodes are pushed to the appropriate peer socket.
   - Incoming frames are parsed, signature-verified, and dispatched to the local `SwarmKernel`.

---

## 8. Security & Governance Integration

1. **Governor Interception**: All operations involving asset movement, external API invocation, or file writes pass through `SecurityGovernor.check_action(...)`.
2. **Air-Gap Quarantine**: Untrusted messages from external nodes cannot invoke local administrative kernel commands without cryptographic authorization from an operator public key.
3. **Audit Trail**: Every routing, join, suspicion, crash, and recovery event is logged to the Omniverse `EventBus` with telemetry tags (`SWARM_PEER_JOIN`, `SWARM_ACTOR_RESTART`, `SWARM_MSG_DLQ`).

---

## 9. Testing & Verification Plan

### 9.1 Unit & Integration Test Suites
- `tests/test_swarm_crypto.py`: Test keypair generation, signature verification, tampered frame rejection, nonce replay rejection.
- `tests/test_swarm_mailbox.py`: Test priority ordering, bounded capacity, backpressure rejection, dead-letter queue.
- `tests/test_swarm_actor.py`: Test actor state transitions, supervisor restart on exception, exponential backoff, max retries termination.
- `tests/test_swarm_gossip.py`: Test SWIM gossip state machine, direct ping, indirect ping-req, and incarnation refutation.
- `tests/test_swarm_transport.py`: Test WebSocket server-client connectivity, frame serialization, reconnection.
- `tests/test_swarm_kernel.py`: Test end-to-end multi-agent dispatch (100+ virtual actors), local vs remote routing, SecurityGovernor gate check, EventBus telemetry.

### 9.2 Benchmark & Performance Targets
- Single-node actor dispatch: $>10,000\text{ messages/sec}$ at $<2\text{ms}$ average latency.
- Cryptographic verification: $>5,000\text{ Ed25519 signatures/sec}$.
- 100% green pass across all existing and new test suites.

---

## 10. CLI Operator Interface

Integrated into the `omniverse` CLI group:
```bash
# Check status of local swarm node, active actors, and peer table
omniverse swarm status

# Start a swarm node listener
omniverse swarm start --port 9091

# Benchmark local actor dispatch and crypto performance
omniverse swarm benchmark --actors 100 --messages 50000
```
