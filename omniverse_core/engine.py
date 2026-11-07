"""
Chronos-Omega Unified Software Engineering & Knowledge Work Engine.
Implements:
1. [PAST]    MerkleAuditLog & DoubleEntryLedger (Cryptographic & ACID invariants)
2. [PRESENT] DAGOrchestrator & ZeroTrustScanner (Multi-Agent DAG & DevSecOps)
3. [FUTURE]  EpistemicKnowledgeEngine & SelfHealingMonitor (GraphRAG & Autonomic Repair)
"""

import hashlib
import json
import math
import re
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


# ============================================================================
# 1. PAST PARADIGM: CRYPTOGRAPHIC MERKLE LOG & ACID DOUBLE-ENTRY LEDGER
# ============================================================================
class MerkleAuditLog:
    """Tamper-evident SHA-256 hash-chained audit log for code & knowledge actions."""

    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = []
        self.head_hash: str = "0" * 64

    def append(self, actor: str, action: str, payload: Dict[str, Any]) -> str:
        timestamp = time.time()
        serialized = json.dumps(payload, sort_keys=True)
        raw = f"{self.head_hash}|{timestamp:.6f}|{actor}|{action}|{serialized}"
        new_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        self.entries.append(
            {
                "index": len(self.entries),
                "timestamp": timestamp,
                "actor": actor,
                "action": action,
                "payload": payload,
                "prev_hash": self.head_hash,
                "hash": new_hash,
            }
        )
        self.head_hash = new_hash
        return new_hash

    def verify_integrity(self) -> bool:
        expected_prev = "0" * 64
        for entry in self.entries:
            if entry["prev_hash"] != expected_prev:
                return False
            serialized = json.dumps(entry["payload"], sort_keys=True)
            raw = (
                f"{expected_prev}|{entry['timestamp']:.6f}|"
                f"{entry['actor']}|{entry['action']}|{serialized}"
            )
            recomputed = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if recomputed != entry["hash"]:
                return False
            expected_prev = entry["hash"]
        return True


class DoubleEntryLedger:
    """ACID Double-Entry Ledger enforcing zero-sum conservation & idempotency."""

    def __init__(self, audit_log: MerkleAuditLog) -> None:
        self.balances: Dict[str, int] = defaultdict(int)
        self.committed_tx_ids: Set[str] = set()
        self.journal: List[Dict[str, Any]] = []
        self.audit = audit_log

    def post_transaction(
        self,
        tx_id: str,
        postings: List[Tuple[str, int]],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        if tx_id in self.committed_tx_ids:
            return False  # Idempotent replay guard
        if not postings or sum(amount for _, amount in postings) != 0:
            raise ValueError(
                "Double-entry invariant violated: postings must sum to 0"
            )
        for account, amount in postings:
            self.balances[account] += amount
        self.committed_tx_ids.add(tx_id)
        record = {
            "tx_id": tx_id,
            "postings": postings,
            "metadata": metadata or {},
        }
        self.journal.append(record)
        self.audit.append("ACID_LEDGER", "POST_TX", record)
        return True

    def verify_conservation(self) -> bool:
        return sum(self.balances.values()) == 0


# ============================================================================
# 2. PRESENT PARADIGM: TOPOLOGICAL DAG ORCHESTRATOR & ZERO-TRUST SCANNER
# ============================================================================
@dataclass
class TaskNode:
    task_id: str
    name: str
    dependencies: List[str]
    fn: Callable[[Dict[str, Any]], Any]


class DAGOrchestrator:
    """Kahn's topological workflow & multi-agent task scheduler with cycle detection."""

    def __init__(self, audit_log: MerkleAuditLog) -> None:
        self.nodes: Dict[str, TaskNode] = {}
        self.audit = audit_log

    def register_task(self, node: TaskNode) -> None:
        self.nodes[node.task_id] = node

    def execute_all(
        self, initial_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        in_degree: Dict[str, int] = {tid: 0 for tid in self.nodes}
        adj: Dict[str, List[str]] = defaultdict(list)
        for tid, node in self.nodes.items():
            for dep in node.dependencies:
                if dep not in self.nodes:
                    raise KeyError(f"Missing dependency '{dep}' for task '{tid}'")
                adj[dep].append(tid)
                in_degree[tid] += 1

        queue = deque([tid for tid, deg in in_degree.items() if deg == 0])
        execution_order: List[str] = []
        results: Dict[str, Any] = dict(initial_context or {})

        while queue:
            curr = queue.popleft()
            execution_order.append(curr)
            node = self.nodes[curr]
            results[curr] = node.fn(results)
            self.audit.append(
                "DAG_ORCHESTRATOR", f"COMPLETE_{curr}", {"task": node.name}
            )
            for nxt in adj[curr]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)

        if len(execution_order) != len(self.nodes):
            raise RuntimeError("Cyclic dependency detected in workflow DAG")
        results["_execution_order"] = execution_order
        return results


class ZeroTrustScanner:
    """Static security & secret scanner enforcing zero-trust code hygiene."""

    PATTERNS = {
        "HARDCODED_SECRET": re.compile(
            r"(?i)(api_key|secret_key|private_key|password)\s*=\s*['\"][A-Za-z0-9_\-]{12,}['\"]"
        ),
        "SQL_INJECTION_RISK": re.compile(
            r"(?i)SELECT\s+.*\s+FROM\s+.*(%s|\+\s*\w+|f['\"])"
        ),
        "DANGEROUS_EVAL": re.compile(r"\b(eval|exec)\s*\("),
    }

    def __init__(self, audit_log: MerkleAuditLog) -> None:
        self.audit = audit_log

    def scan_source(self, filename: str, content: str) -> List[Dict[str, str]]:
        findings: List[Dict[str, str]] = []
        for rule_name, pattern in self.PATTERNS.items():
            for match in pattern.finditer(content):
                findings.append(
                    {
                        "file": filename,
                        "rule": rule_name,
                        "match": match.group(0)[:40],
                    }
                )
        self.audit.append(
            "ZERO_TRUST_SCANNER",
            "SCAN_FILE",
            {"file": filename, "findings_count": len(findings)},
        )
        return findings


# ============================================================================
# 3. FUTURE PARADIGM: EPISTEMIC KNOWLEDGE ENGINE & AUTONOMIC SELF-HEALER
# ============================================================================
class EpistemicKnowledgeEngine:
    """
    Hybrid BM25 + Knowledge-Graph Entity-Boosted Retrieval & Synthesis Engine
    for citation-grounded Knowledge Work and ADR/PRD generation.
    """

    def __init__(self, audit_log: MerkleAuditLog) -> None:
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.entity_index: Dict[str, Set[str]] = defaultdict(set)
        self.audit = audit_log

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return [
            t.strip(".,!?:;()[]{}\"'").lower()
            for t in text.split()
            if t.strip(".,!?:;()[]{}\"'")
        ]

    def ingest_document(
        self, doc_id: str, title: str, content: str, entities: List[str]
    ) -> None:
        tokens = self._tokenize(content)
        norm_entities = {e.lower() for e in entities}
        self.documents[doc_id] = {
            "doc_id": doc_id,
            "title": title,
            "content": content,
            "tokens": tokens,
            "entities": norm_entities,
        }
        for ent in norm_entities:
            self.entity_index[ent].add(doc_id)
        self.audit.append(
            "EPISTEMIC_ENGINE",
            "INGEST_DOC",
            {"doc_id": doc_id, "title": title, "entities": list(norm_entities)},
        )

    def synthesize_answer(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        q_tokens = self._tokenize(query)
        n_docs = max(len(self.documents), 1)
        avgdl = (
            sum(len(d["tokens"]) for d in self.documents.values()) / n_docs
            if self.documents
            else 1.0
        )
        scored: List[Tuple[float, str]] = []

        for doc_id, doc in self.documents.items():
            score = 0.0
            dl = max(len(doc["tokens"]), 1)
            for qt in q_tokens:
                tf = doc["tokens"].count(qt)
                if tf > 0:
                    df = sum(
                        1 for d in self.documents.values() if qt in d["tokens"]
                    )
                    idf = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))
                    k1, b = 1.5, 0.75
                    score += idf * (
                        (tf * (k1 + 1.0))
                        / (tf + k1 * (1.0 - b + b * (dl / avgdl)))
                    )
                if qt in doc["entities"]:
                    score += 2.5  # Knowledge Graph entity link boost
            if score > 0:
                scored.append((score, doc_id))

        scored.sort(key=lambda item: item[0], reverse=True)
        evidence = []
        for sc, doc_id in scored[:top_k]:
            doc = self.documents[doc_id]
            evidence.append(
                {
                    "doc_id": doc_id,
                    "title": doc["title"],
                    "relevance_score": round(sc, 4),
                    "citation": f"[{doc_id}: {doc['title']}]",
                    "verified_excerpt": doc["content"],
                }
            )

        synthesis = (
            " | ".join(
                f"{item['citation']} {item['verified_excerpt']}"
                for item in evidence
            )
            if evidence
            else "INSUFFICIENT_EPISTEMIC_EVIDENCE"
        )
        return {
            "query": query,
            "epistemic_verified": len(evidence) > 0,
            "citations": [item["citation"] for item in evidence],
            "synthesis": synthesis,
            "evidence": evidence,
        }


class SelfHealingMonitor:
    """Z-score anomaly detector that triggers automatic remediation callbacks."""

    def __init__(self, audit_log: MerkleAuditLog) -> None:
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.remediations: Dict[str, Callable[[float], str]] = {}
        self.audit = audit_log

    def register_remediation(
        self, metric_name: str, handler: Callable[[float], str]
    ) -> None:
        self.remediations[metric_name] = handler

    def record_observation(
        self, metric_name: str, value: float
    ) -> Optional[Dict[str, Any]]:
        history = self.metrics[metric_name]
        if len(history) >= 5:
            mean = sum(history) / len(history)
            variance = sum((x - mean) ** 2 for x in history) / len(history)
            std = max(math.sqrt(variance), 1e-6)
            z_score = abs(value - mean) / std
            if z_score > 3.0:
                action_taken = "ALERT_LOGGED"
                if metric_name in self.remediations:
                    action_taken = self.remediations[metric_name](value)
                event = {
                    "metric": metric_name,
                    "anomalous_value": value,
                    "z_score": round(z_score, 2),
                    "remediation": action_taken,
                }
                self.audit.append("SELF_HEALER", "AUTO_REMEDIATE", event)
                history.append(value)
                return event
        history.append(value)
        return None
