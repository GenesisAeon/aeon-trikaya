from collections.abc import Iterable
from pathlib import Path
from statistics import mean, variance
from typing import Any

from .archetype_tools import get_symbol
from .symbol_tools import assign_color
from .trikaya import trikaya_state


def pearson_corr(xs: list[float], ys: list[float]) -> float:
    """Return Pearson correlation coefficient for two equal-length lists."""
    n = len(xs)
    if n != len(ys) or n == 0:
        return 0.0
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = float(sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys, strict=False)))
    den_x: float = sum((x - mean_x) ** 2 for x in xs) ** 0.5
    den_y: float = sum((y - mean_y) ** 2 for y in ys) ** 0.5
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / (den_x * den_y)


def sonify(values: Iterable[float]) -> list[float]:
    """Map numeric values to simple tone frequencies."""
    return [440.0 + v * 40.0 for v in values]


def visualize_light(values: Iterable[float]) -> list[str]:
    """Map numeric values to HSL color strings."""
    colors = []
    for v in values:
        hue = int((v % 1) * 360)
        colors.append(f"hsl({hue},70%,50%)")
    return colors


def assign_symbol(values: Iterable[float], context: str | None = None) -> str:
    """Assign a symbolic marker based on the average value.

    If ``context`` is provided, ``archetypes.yaml`` is consulted to map the
    value to an archetype specific symbol. When no archetype matches, the
    default mapping from the project guidelines is used:

    - avg > 0.8 -> sun symbol (☀)
    - avg > 0.6 -> fire archetype (🔥)
    - avg > 0.4 -> growth symbol (🌱)
    - avg > 0.2 -> fluid symbol (💧)
    - otherwise -> void symbol (⚫)
    """
    vals = list(values)
    avg = sum(vals) / len(vals) if vals else 0

    if context:
        cfg = Path(__file__).with_name("archetypes.yaml")
        symbol, _ = get_symbol(avg, context, cfg)
        if symbol != "⚫":
            return symbol

    if avg > 0.8:
        return "\u2600"  # sun
    elif avg > 0.6:
        return "\U0001F525"  # fire
    elif avg > 0.4:
        return "\U0001F331"  # sprout
    elif avg > 0.2:
        return "\U0001F4A7"  # droplet
    else:
        return "\u26AB"  # void


def translate_numeric_to_symbolic(tensor: Iterable[float]) -> dict[str, Any]:
    """Translate numeric input into symbolic representations."""
    vals = list(map(float, tensor))
    return {
        "klang": sonify(vals),
        "licht": visualize_light(vals),
        "symbol": assign_symbol(vals),
    }


def CREP_eval(symbolic_data: dict[str, Any]) -> int:
    """Very rough CREP evaluation returning -1, 0 or 1."""
    freq_avg = sum(symbolic_data["klang"]) / len(symbolic_data["klang"])
    if freq_avg > 500:
        return 1
    if freq_avg < 440:
        return -1
    return 0


def advanced_crep_eval(
    symbolic_data: dict[str, Any], prev_states: list[dict[str, Any]] | None = None
) -> dict[str, float]:
    """Calculate basic CREP metrics.

    Parameters
    ----------
    symbolic_data:
        Dictionary containing at least "klang" list.
    prev_states:
        Optional list of previous symbolic states to compute resonance.
    """

    klang = [float(f) for f in symbolic_data.get("klang", [])]
    coherence = variance(klang) if len(klang) > 1 else 0.0
    presence = mean(klang) if klang else 0.0

    resonance = 0.0
    if prev_states:
        correlations = []
        for state in prev_states:
            prev = [float(f) for f in state.get("klang", [])]
            m = min(len(prev), len(klang))
            if m:
                correlations.append(pearson_corr(prev[:m], klang[:m]))
        if correlations:
            resonance = sum(correlations) / len(correlations)

    emergence = (
        mean(abs(klang[i] - klang[i - 1]) for i in range(1, len(klang)))
        if len(klang) > 1
        else 0.0
    )

    emergence_clusters = 0
    if len(klang) > 1:
        emergence_clusters = sum(
            1 for i in range(1, len(klang)) if abs(klang[i] - klang[i - 1]) > 0.5
        )

    return {
        "kohärenz": coherence,
        "resonanz": resonance,
        "emergenz": emergence,
        "emergenz_cluster": float(emergence_clusters),
        "präsenz": presence,
    }


def refactor_fraktal(symbolic_data: dict[str, Any]) -> dict[str, Any]:
    """Simple refactoring: invert frequencies."""
    symbolic_data["klang"] = [440 - (f - 440) for f in symbolic_data["klang"]]
    return symbolic_data


def fraktal_feedback(data: Iterable[float], depth: int = 3) -> tuple[dict[str, Any], int]:
    """Recursive fractal feedback loop with basic CREP evaluation."""
    symbolic = translate_numeric_to_symbolic(data)
    score = -1
    for _ in range(depth):
        score = CREP_eval(symbolic)
        if score == -1:
            symbolic = refactor_fraktal(symbolic)
        else:
            break
    return symbolic, score


def fraktal_feedback_metrics(
    data: Iterable[float],
    depth: int = 3,
    prev_states: list[dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], int, dict[str, float]]:
    """Fractal feedback that also returns CREP metric dictionary."""
    symbolic = translate_numeric_to_symbolic(data)
    states = list(prev_states or [])
    score = -1
    metrics: dict[str, float] = {}
    for _ in range(depth):
        score = CREP_eval(symbolic)
        metrics = advanced_crep_eval(symbolic, states[-1:] if states else None)
        states.append(symbolic)
        if score == -1:
            symbolic = refactor_fraktal(symbolic)
        else:
            break
    return symbolic, score, metrics


def fraktal_feedback_graph(data: Iterable[float], depth: int = 3) -> dict[str, Any]:
    """Return a simple graph representation of the feedback process."""
    if depth <= 0:
        return {"nodes": [], "edges": []}

    symbolic = translate_numeric_to_symbolic(data)
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, int]] = []
    states: list[dict[str, Any]] = []

    if not symbolic.get("klang"):
        nodes.append({"id": 0, "state": symbolic, "metrics": {}, "trikaya_state": trikaya_state(0)})
        return {"nodes": nodes, "edges": edges}

    for step in range(depth):
        metrics = advanced_crep_eval(symbolic, states[-1:] if states else None)
        score = CREP_eval(symbolic)
        nodes.append({
            "id": step,
            "state": symbolic,
            "metrics": metrics,
            "trikaya_state": trikaya_state(score),
        })
        states.append(symbolic)
        if score == -1 and step < depth - 1:
            symbolic = refactor_fraktal(dict(symbolic))
            edges.append({"from": step, "to": step + 1})
        else:
            break

    return {"nodes": nodes, "edges": edges}


def generate_haiku(symbolic_data: dict[str, Any]) -> str:
    """Generate a simple haiku description for the symbolic output.

    This function maps the assigned symbol to a short three line poem.
    The haiku texts are intentionally minimal and deterministic so that
    tests can assert on the exact output without relying on randomness
    or external APIs.
    """

    symbol = symbolic_data.get("symbol")
    if symbol == "\u2600":  # ☀️
        return "golden light rises\nseeds awaken to the day\nclarity unfolds"
    if symbol == "\U0001F331":  # 🌱
        return "tender shoots emerge\nsoil carries silent promise\nnew roots find their depth"
    if symbol == "\U0001F4A7":  # 💧
        return "raindrops softly fall\npooling into quiet streams\nchange flows ever on"
    # default case for ⚫ or unknown symbol
    return "stillness all around\nshadows weave an empty path\nnight consumes the sound"



def generate_poetic_commentary(metrics: dict[str, float]) -> str:
    """Return a short deterministic poetic line based on CREP metrics."""
    avg = sum(metrics.values()) / len(metrics) if metrics else 0.0
    if avg >= 0.8:
        return "resonant patterns bloom"
    if avg >= 0.5:
        return "subtle waves converge"
    return "quiet traces fade"


def symbolic_manifestation(values: Iterable[float]) -> dict[str, Any]:
    """Return symbolic data, haiku and color for input values."""
    vals = list(map(float, values))
    symbolic = translate_numeric_to_symbolic(vals)
    haiku = generate_haiku(symbolic)
    avg = sum(vals) / len(vals) if vals else 0.0
    color = assign_color(avg)
    return {"symbolic": symbolic, "haiku": haiku, "color": color}
