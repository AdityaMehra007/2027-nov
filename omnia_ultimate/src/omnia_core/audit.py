from __future__ import annotations
import hashlib
import json
import time
from typing import Any

GENESIS = "0" * 64

def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def event_hash(previous_hash: str, event: dict[str, Any]) -> str:
    body = {"previous_hash": previous_hash, "event": event}
    return hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()

def make_event(event_type: str, aggregate_id: str, actor: str, payload: dict[str, Any],
               previous_hash: str) -> dict[str, Any]:
    core = {
        "event_id": hashlib.sha256(f"{time.time_ns()}:{aggregate_id}:{event_type}".encode()).hexdigest()[:32],
        "event_type": event_type,
        "aggregate_id": aggregate_id,
        "actor": actor,
        "payload": payload,
        "occurred_at": time.time(),
    }
    digest = event_hash(previous_hash, core)
    return {**core, "previous_hash": previous_hash, "event_hash": digest}

def verify_chain(events: list[dict[str, Any]]) -> bool:
    previous = GENESIS
    for event in events:
        core = {k: event[k] for k in (
            "event_id", "event_type", "aggregate_id", "actor", "payload", "occurred_at"
        )}
        if event.get("previous_hash") != previous:
            return False
        calculated = event_hash(previous, core)
        if event.get("event_hash") != calculated:
            return False
        previous = calculated
    return True
