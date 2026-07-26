from __future__ import annotations

import json
import statistics
import time
from collections.abc import Iterable
from pathlib import Path
from typing import Any


def store_result(
    result: dict[str, Any],
    path: Path,
    *,
    mood: str | None = None,
    archetype: str | None = None,
) -> None:
    """Append result to a JSON list stored at path.

    Additional metadata ``mood`` and ``archetype`` can be provided and will be
    stored with each entry.
    """
    if path.exists():
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    entry = dict(result)
    entry.setdefault("timestamp", time.time())
    if mood is not None:
        entry["mood"] = mood
    if archetype is not None:
        entry["archetype"] = archetype
    data.append(entry)
    path.write_text(json.dumps(data, indent=2))


def load_results(path: Path) -> list[dict[str, Any]]:
    """Load list of stored results or return empty list."""
    if path.exists():
        try:
            data: list[dict[str, Any]] = json.loads(path.read_text())
            return data
        except json.JSONDecodeError:
            return []
    return []


def summarize_entries(results: Iterable[dict[str, Any]]) -> dict[str, float]:
    """Return average values for numeric fields in ``results``."""
    sums: dict[str, list[float]] = {}
    for entry in results:
        for key, value in entry.items():
            if isinstance(value, (int, float)):
                sums.setdefault(key, []).append(float(value))

    return {k: sum(v) / len(v) for k, v in sums.items() if v}


def summarize_stats(results: Iterable[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Return mean and median for numeric fields in ``results``."""
    values: dict[str, list[float]] = {}
    for entry in results:
        for key, value in entry.items():
            if isinstance(value, (int, float)):
                values.setdefault(key, []).append(float(value))

    stats = {}
    for key, vals in values.items():
        if vals:
            mean = sum(vals) / len(vals)
            med = statistics.median(vals)
            stats[key] = {"mean": mean, "median": med}
    return stats


def summarize_stats_memory(path: Path) -> dict[str, dict[str, float]]:
    """Return mean and median statistics for numeric fields stored in ``path``."""
    results = load_results(path)
    if not results:
        return {}
    return summarize_stats(results)


def summarize_memory(path: Path) -> dict[str, float]:
    """Return simple averages for numeric fields in stored results."""
    results = load_results(path)
    if not results:
        return {}

    return summarize_entries(results)


def tail_results(path: Path, n: int = 10) -> list[dict[str, Any]]:
    """Return the last ``n`` stored results.

    Parameters
    ----------
    path:
        Path to the JSON memory file.
    n:
        Number of entries to retrieve from the end of the file.
    """
    results = load_results(path)
    if not results:
        return []
    return results[-n:]


def trend_metric(path: Path, key: str, n: int = 5) -> float | None:
    """Return average stepwise change for ``key`` in the last ``n`` entries.

    Parameters
    ----------
    path:
        Path to the JSON memory file.
    key:
        Numeric field to analyze.
    n:
        Number of recent entries to evaluate.
    """
    entries = tail_results(path, n)
    values: list[float] = []
    for e in entries:
        v = e.get(key)
        if isinstance(v, (int, float)):
            values.append(float(v))
    if len(values) < 2:
        return None
    diffs = [values[i] - values[i - 1] for i in range(1, len(values))]
    return sum(diffs) / len(diffs)


def volatility_metric(results: Iterable[dict[str, Any]]) -> dict[str, float]:
    """Return standard deviation for numeric fields in ``results``."""
    values: dict[str, list[float]] = {}
    for entry in results:
        for key, value in entry.items():
            if isinstance(value, (int, float)):
                values.setdefault(key, []).append(float(value))

    volatilities: dict[str, float] = {}
    for key, vals in values.items():
        if len(vals) > 1:
            mean_val = sum(vals) / len(vals)
            var = sum((v - mean_val) ** 2 for v in vals) / len(vals)
            volatilities[key] = var ** 0.5
        else:
            volatilities[key] = 0.0
    return volatilities


def volatility_metric_memory(path: Path) -> dict[str, float]:
    """Return :func:`volatility_metric` for JSON data stored in ``path``."""
    results = load_results(path)
    if not results:
        return {}
    return volatility_metric(results)

