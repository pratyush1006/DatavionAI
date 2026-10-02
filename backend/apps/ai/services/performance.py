from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from statistics import mean
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class PerformanceSummary:
    count: int
    elapsed_seconds: float
    average_seconds: float
    throughput_per_second: float
    failures: int


def benchmark_concurrent(
    call: Callable[[], T],
    *,
    concurrency: int = 4,
    iterations: int = 8,
) -> PerformanceSummary:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    concurrency = max(1, int(concurrency))
    iterations = max(1, int(iterations))

    start = time.perf_counter()
    durations: list[float] = []
    failures = 0

    def one() -> tuple[float, bool]:
        began = time.perf_counter()
        try:
            call()
            return time.perf_counter() - began, True
        except Exception:
            return time.perf_counter() - began, False

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(one) for _ in range(iterations)]
        for future in as_completed(futures):
            duration, ok = future.result()
            durations.append(duration)
            if not ok:
                failures += 1

    elapsed = max(time.perf_counter() - start, 0.000001)
    return PerformanceSummary(
        count=iterations,
        elapsed_seconds=elapsed,
        average_seconds=mean(durations) if durations else 0.0,
        throughput_per_second=iterations / elapsed,
        failures=failures,
    )
