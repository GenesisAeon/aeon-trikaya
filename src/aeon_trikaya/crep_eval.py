"""Minimal CREP evaluation module."""

from typing import Any


def evaluate_crep(input_data: Any) -> dict[str, float]:
    """Return static CREP metrics for a given input."""
    return {
        "coherence": 0.85,
        "resonance": 0.75,
        "emergence": 0.65,
        "presence": 1.0,
    }
