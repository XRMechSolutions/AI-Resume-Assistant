"""Per-host spacing for HTTP calls and human-paced waits for the browser."""

import asyncio
import random
import time


class Pacer:
    def __init__(self, min_interval_s: float, clock=time.monotonic, sleep=asyncio.sleep):
        self._min = min_interval_s
        self._last: dict[str, float] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self._clock = clock
        self._sleep = sleep

    async def wait(self, host: str) -> None:
        lock = self._locks.setdefault(host, asyncio.Lock())
        async with lock:
            gap = self._clock() - self._last.get(host, float("-inf"))
            if gap < self._min:
                await self._sleep(self._min - gap)
            self._last[host] = self._clock()


async def human_pause(bounds: tuple[float, float], sleep=asyncio.sleep) -> float:
    delay = random.uniform(*bounds)
    await sleep(delay)
    return delay
