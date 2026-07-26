from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any


def load_sigil(path: Path) -> dict[str, Any]:
    """Load sigil JSON file and return parsed data.

    Parameters
    ----------
    path:
        Path to a JSON file containing a sigil structure.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Sigil file not found: {path}") from e
    try:
        data: dict[str, Any] = json.loads(text)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid sigil JSON: {e}") from e


def load_start_sigil() -> dict[str, Any]:
    """Load the packaged ``StartSigil.json`` file.

    This helper allows tools like :mod:`~aeon_trikaya.aeon_cli` to
    easily include the project\'s default sigil without requiring an explicit
    file path.
    """
    assert __package__ is not None
    with resources.files(__package__).joinpath("StartSigil.json").open(
        "r", encoding="utf-8"
    ) as f:
        data: dict[str, Any] = json.load(f)
        return data
