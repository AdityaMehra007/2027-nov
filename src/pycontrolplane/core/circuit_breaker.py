import time
from enum import Enum
from typing import Optional


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreakerOpenException(Exception):
    """Raised when an operation is rejected by an open circuit breaker."""
    pass


class CircuitBreaker:
    """Enterprise-grade Circuit Breaker finite state machine.
    
    State Transitions:
      - CLOSED -> OPEN: Triggered when failure count reaches failure_threshold.
      - OPEN -> HALF_OPEN: Occurs after recovery_timeout_sec has elapsed.
      - HALF_OPEN -> CLOSED: Occurs when half_open_success_threshold consecutive calls succeed.
      - HALF_OPEN -> OPEN: Occurs immediately if any call fails during HALF_OPEN probe.
    """

    def __init__(
        self,
        name: str = "default_breaker",
        failure_threshold: int = 5,
        recovery_timeout_sec: float = 10.0,
        half_open_success_threshold: int = 2,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.half_open_success_threshold = half_open_success_threshold

        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.success_count: int = 0
        self.last_state_change: float = time.time()
        self.last_failure_time: float = 0.0

    def check_execution(self) -> bool:
        """Determines if a request can proceed through the circuit breaker."""
        now = time.time()

        if self.state == CircuitState.OPEN:
            if now - self.last_failure_time >= self.recovery_timeout_sec:
                self._transition_to(CircuitState.HALF_OPEN)
                self.success_count = 0
                return True
            else:
                remaining = self.recovery_timeout_sec - (now - self.last_failure_time)
                raise CircuitBreakerOpenException(
                    f"Circuit '{self.name}' is OPEN. Retry in {remaining:.2f}s"
                )

        return True

    def record_success(self) -> None:
        """Records a successful operation."""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_success_threshold:
                self._transition_to(CircuitState.CLOSED)
                self.failure_count = 0
                self.success_count = 0
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0

    def record_failure(self) -> None:
        """Records a failed operation."""
        now = time.time()
        self.last_failure_time = now

        if self.state == CircuitState.CLOSED:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self._transition_to(CircuitState.OPEN)
        elif self.state == CircuitState.HALF_OPEN:
            self._transition_to(CircuitState.OPEN)

    def trip(self) -> None:
        """Manually force the circuit breaker into OPEN state (used in SRE self-healing)."""
        self.last_failure_time = time.time()
        self._transition_to(CircuitState.OPEN)

    def reset(self) -> None:
        """Manually reset the circuit breaker back to CLOSED state."""
        self.failure_count = 0
        self.success_count = 0
        self._transition_to(CircuitState.CLOSED)

    def _transition_to(self, new_state: CircuitState) -> None:
        self.state = new_state
        self.last_state_change = time.time()
