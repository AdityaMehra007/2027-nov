import time
from typing import List, Dict, Any

class EventBus:
    """Thread-safe event logging and telemetry bus."""

    def __init__(self):
        self._events: List[Dict[str, Any]] = []

    def publish(self, event_name: str, payload: Dict[str, Any]) -> None:
        event = {
            "timestamp": time.time(),
            "event_name": event_name,
            "payload": payload
        }
        self._events.append(event)

    def get_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self._events[-limit:]

    def clear(self) -> None:
        self._events.clear()

global_event_bus = EventBus()
