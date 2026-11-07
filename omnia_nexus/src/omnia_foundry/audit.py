from __future__ import annotations
import hashlib, json, time, uuid
from typing import Any

GENESIS = "0" * 64

def canonical(obj: dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def make_event(kind: str, object_id: str, actor: str, payload: dict[str, Any], previous: str) -> dict[str, Any]:
    core = {
        "event_id": uuid.uuid4().hex,
        "kind": kind,
        "object_id": object_id,
        "actor": actor,
        "payload": payload,
        "timestamp": time.time(),
    }
    digest = hashlib.sha256(canonical({"previous_hash": previous, "event": core}).encode()).hexdigest()
    return {**core, "previous_hash": previous, "event_hash": digest}

def verify(events: list[dict[str, Any]]) -> bool:
    previous = GENESIS
    for e in events:
        core = {k: e[k] for k in ("event_id", "kind", "object_id", "actor", "payload", "timestamp")}
        if e.get("previous_hash") != previous:
            return False
        expected = hashlib.sha256(canonical({"previous_hash": previous, "event": core}).encode()).hexdigest()
        if e.get("event_hash") != expected:
            return False
        previous = expected
    return True
