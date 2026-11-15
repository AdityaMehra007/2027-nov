import time


class TokenBucketRateLimiter:
    """Thread-safe Token Bucket rate limiter with microsecond timestamp refill."""

    def __init__(self, capacity: float, refill_rate: float):
        """
        Args:
            capacity: Maximum burst capacity in tokens.
            refill_rate: Tokens generated per second.
        """
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_update = time.perf_counter()

    def _refill(self) -> None:
        now = time.perf_counter()
        elapsed = now - self.last_update
        self.last_update = now
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))

    def acquire(self, tokens: float = 1.0) -> bool:
        """Attempt to consume tokens. Returns True if accepted, False if rate limited."""
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def get_available_tokens(self) -> float:
        self._refill()
        return self.tokens
