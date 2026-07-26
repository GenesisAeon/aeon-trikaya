"""Utilities for loading plug-in manifests."""

import json
from pathlib import Path
from typing import Any

import yaml

REQUIRED_FIELDS = {"id", "type", "entry"}


def load_plugin_manifest(path: Path) -> dict[str, Any]:
    """Load a single plugin manifest from YAML or JSON."""
    if not path.exists():
        raise FileNotFoundError(f"Plugin manifest not found: {path}")
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Plugin manifest must be a mapping")
    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(sorted(missing))}")
    return data


def load_plugins(directory: Path) -> dict[str, dict[str, Any]]:
    """Load all plugin manifests from a directory."""
    plugins: dict[str, dict[str, Any]] = {}
    for pattern in ("*.yaml", "*.yml", "*.json"):
        for path in directory.glob(pattern):
            manifest = load_plugin_manifest(path)
            plugins[manifest["id"]] = manifest
    return plugins
