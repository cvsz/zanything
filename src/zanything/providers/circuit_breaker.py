"""Circuit breaker pattern for provider resilience and fault tolerance."""

import time
from enum import StrEnum

from zanything.logging import get_logger

logger = get_logger("zanything.providers.circuit_breaker")


class CircuitState(StrEnum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, fast-reject requests
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreakerOpenError(Exception):
    """Raised when request is rejected because circuit is OPEN."""

    pass


class CircuitBreaker:
    """Stateful circuit breaker tracking failure rates and recovery timeouts."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 3,
        recovery_timeout_seconds: float = 10.0,
    ) -> None:
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_state_change = time.time()

    def record_success(self) -> None:
        """Record successful execution, resetting failure count and closing circuit."""
        if self.state != CircuitState.CLOSED:
            logger.info(f"CircuitBreaker '{self.name}' closed (recovered).")
        self.state = CircuitState.CLOSED
        self.failure_count = 0

    def record_failure(self) -> None:
        """Record execution failure, potentially opening the circuit."""
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.last_state_change = time.time()
            logger.error(
                f"CircuitBreaker '{self.name}' opened after "
                f"{self.failure_count} failures."
            )

    def allow_request(self) -> bool:
        """Determine if request is permitted or if circuit is open."""
        now = time.time()
        if self.state == CircuitState.OPEN:
            if now - self.last_state_change > self.recovery_timeout_seconds:
                self.state = CircuitState.HALF_OPEN
                logger.info(f"CircuitBreaker '{self.name}' entered HALF_OPEN state.")
                return True
            return False
        return True
