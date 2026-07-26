from pathlib import Path
from typing import Any

import yaml


def load_archetypes(path: Path) -> list[dict[str, Any]]:
    """Load archetype config from YAML file."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def get_symbol(
    crep: float, context: str, config_path: Path | str = Path("archetypes.yaml")
) -> tuple[str, str]:
    """Return symbol and meaning for given CREP value and context."""
    path = Path(config_path)
    if not path.exists():
        return "⚫", "Unbestimmt"
    archetypes = load_archetypes(path)
    for entry in archetypes:
        try:
            crep_min = float(entry.get("crep_min", 0) or 0)
            crep_max = float(entry.get("crep_max", 0) or 0)
            if entry.get("context") == context and crep_min <= crep <= crep_max:
                symbol = str(entry.get("symbol", "⚫"))
                meaning = str(entry.get("meaning", "Unbestimmt"))
                return symbol, meaning
        except (TypeError, ValueError):
            continue
    return "⚫", "Unbestimmt"
