import time
import json
import hashlib
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional


@dataclass
class AuditRecord:
    index: int
    timestamp: float
    actor: str
    action: str
    payload: Dict[str, Any]
    prev_hash: str
    current_hash: str


class MerkleAuditLedger:
    """Tamper-evident cryptographically chained audit log for enterprise operations."""

    GENESIS_HASH = "0" * 64

    def __init__(self):
        self.records: List[AuditRecord] = []

    def _hash_record(
        self,
        index: int,
        timestamp: float,
        actor: str,
        action: str,
        payload: Dict[str, Any],
        prev_hash: str,
    ) -> str:
        serialized_payload = json.dumps(payload, sort_keys=True)
        raw = f"{index}|{timestamp:.6f}|{actor}|{action}|{serialized_payload}|{prev_hash}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def append_record(self, actor: str, action: str, payload: Dict[str, Any]) -> AuditRecord:
        index = len(self.records)
        timestamp = time.time()
        prev_hash = self.records[-1].current_hash if self.records else self.GENESIS_HASH
        current_hash = self._hash_record(index, timestamp, actor, action, payload, prev_hash)

        record = AuditRecord(
            index=index,
            timestamp=timestamp,
            actor=actor,
            action=action,
            payload=payload,
            prev_hash=prev_hash,
            current_hash=current_hash,
        )
        self.records.append(record)
        return record

    def verify_chain_integrity(self) -> bool:
        """Verifies the unbroken SHA-256 Merkle chain from genesis to head."""
        for i, rec in enumerate(self.records):
            expected_prev = self.records[i - 1].current_hash if i > 0 else self.GENESIS_HASH
            if rec.prev_hash != expected_prev:
                return False

            recalculated_hash = self._hash_record(
                rec.index,
                rec.timestamp,
                rec.actor,
                rec.action,
                rec.payload,
                rec.prev_hash,
            )
            if rec.current_hash != recalculated_hash:
                return False

        return True
