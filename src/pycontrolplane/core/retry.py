import time
import random
from typing import Callable, Any, Optional, Tuple, Type


class RetryPolicy:
    """Configurable exponential backoff retry policy with full jitter."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay_sec: float = 0.05,
        backoff_factor: float = 2.0,
        max_delay_sec: float = 5.0,
        jitter: bool = True,
        retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
    ):
        self.max_retries = max_retries
        self.initial_delay_sec = initial_delay_sec
        self.backoff_factor = backoff_factor
        self.max_delay_sec = max_delay_sec
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions or (Exception,)

    def compute_delay(self, attempt: int) -> float:
        delay = self.initial_delay_sec * (self.backoff_factor ** attempt)
        delay = min(delay, self.max_delay_sec)
        if self.jitter:
            delay = random.uniform(0.0, delay)
        return delay


class ResilienceExecutor:
    """Resilient execution wrapper applying retries, backoff, and circuit integration."""

    def __init__(self, retry_policy: Optional[RetryPolicy] = None):
        self.retry_policy = retry_policy or RetryPolicy()

    def execute(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        last_exception: Optional[Exception] = None
        for attempt in range(self.retry_policy.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except self.retry_policy.retryable_exceptions as e:
                last_exception = e
                if attempt == self.retry_policy.max_retries:
                    break
                delay = self.retry_policy.compute_delay(attempt)
                time.sleep(delay)

        if last_exception is not None:
            raise last_exception
        raise RuntimeError("Resilience execution failed without explicit exception")
