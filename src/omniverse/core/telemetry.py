import json
import time
import threading
from pathlib import Path
from typing import List, Dict, Any

class EventBus:
    """Thread-safe event logging and telemetry bus."""

    def __init__(self, log_path: str = "artifacts/telemetry/events.jsonl"):
        self._events: List[Dict[str, Any]] = []
        self._log_path = Path(log_path)
        self._lock = threading.Lock()

    def publish(self, event_name: str, payload: Dict[str, Any]) -> None:
        event = {
            "timestamp": time.time(),
            "event_name": event_name,
            "payload": payload
        }
        with self._lock:
            self._events.append(event)
            try:
                self._log_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self._log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(event, default=str) + "\n")
            except Exception:
                pass

    def get_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._events[-limit:])

    def clear(self) -> None:
        with self._lock:
            self._events.clear()

global_event_bus = EventBus()
