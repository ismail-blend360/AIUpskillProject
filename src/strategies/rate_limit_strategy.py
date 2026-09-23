"""Rate limiting strategies."""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class RateLimitStrategy(ABC):
    """Abstract strategy for rate limiting."""

    @abstractmethod
    async def acquire(self):
        """Acquire permission to make request."""
        pass

    @abstractmethod
    def release(self):
        """Release permission after request."""
        pass


class SemaphoreStrategy(RateLimitStrategy):
    """
    Simple semaphore-based rate limiting.

    Limits concurrent requests.
    """

    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def acquire(self):
        await self.semaphore.acquire()

    def release(self):
        self.semaphore.release()


class TokenBucketStrategy(RateLimitStrategy):
    """
    Token bucket rate limiting.

    Allows bursts but limits over time.
    """

    def __init__(self, rate: int, per: float):
        """
        Initialize token bucket.

        Args:
            rate: Number of requests
            per: Time period in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = datetime.now()

    async def acquire(self):
        current = datetime.now()
        time_passed = (current - self.last_check).total_seconds()
        self.last_check = current

        self.allowance += time_passed * (self.rate / self.per)
        if self.allowance > self.rate:
            self.allowance = self.rate

        if self.allowance < 1.0:
            sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
            await asyncio.sleep(sleep_time)
            self.allowance = 0.0
        else:
            self.allowance -= 1.0

    def release(self):
        pass  # Not needed for token bucket
