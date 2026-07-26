import time
import tracemalloc
from collections.abc import Iterable
from typing import Any

from .aeon_processor import fraktal_feedback


def monitor_performance(data: Iterable[float], depth: int = 3) -> dict[str, Any]:
    """Run fraktal_feedback and measure execution metrics."""
    tracemalloc.start()
    start = time.perf_counter()
    result = fraktal_feedback(data, depth)
    duration = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "result": result,
        "duration": duration,
        "peak_memory": peak,
    }
