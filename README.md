# aeon-trikaya (GenesisAeon Package 52)

Fractal CREP feedback and Trikaya state classification for numeric-to-symbolic
sensemaking. Ported from `unified-mandala/GenesisAeonAdvancedAi/`.

## What this is

A rule-based (not machine-learning) pipeline: numeric input is translated
into "symbolic" form (tone frequencies, HSL colors, a glyph), scored with a
discrete CREP heuristic, classified into one of three Trikaya states
(PRÄSENZ / LEERE / AUFLÖSUNG), optionally refined through a fractal
refeedback loop, and persisted with trend/volatility analytics over time.
Includes a CLI, a minimal Flask API, and deterministic haiku/poetry
generation.

This is a genuine, working precursor to a much larger aspirational
"AeonNeuroNetz" vision (neural core, VR, Mandala-UI - see
`docs/blueprints/`) - **not** that vision itself. See
[`epistemic_status.md`](epistemic_status.md) for the full, honest
breakdown of what's real vs. aspirational, including two corrections to
the original extraction prompt (Trikaya is a discrete lookup, not a
continuous threshold; one module, `crep_eval.py`, is a non-functional
stub kept for API compatibility).

## Install

```bash
pip install -e .                    # core
pip install -e ".[plotting]"        # + feedback-graph / mandala visualization
pip install -e ".[flask]"           # + minimal HTTP API
```

## Quick start

```python
from aeon_trikaya import AeonTrikayaSystem

system = AeonTrikayaSystem(depth=3)
result = system.run_cycle(input_values=[0.1, 0.2, 0.3])
print(system.get_trikaya_state())  # e.g. "AUFLÖSUNG"
```

Or via the CLI (ported as-is):

```bash
python -m aeon_trikaya.aeon_cli 0.1 0.2 0.3 --haiku --graph
```

## Diamond Interface

Implements the six-method [GenesisAeon Diamond Interface](https://github.com/GenesisAeon/diamond-setup)
via `AeonTrikayaSystem`, plus a bonus `get_trikaya_state()`. See
`epistemic_status.md` for exactly how CREP/UTAC fields are derived from
this package's real, discrete scoring (not fabricated to fit the contract).

## Ecosystem relationship

Diffed against `aeon-ai` before extraction (see
`unified-mandala/MANDALA_MAP.md`, 2026-07-26): genuine but modest overlap
(~20% of modules have more capable equivalents there); the rest - Trikaya
classification, fractal feedback, persistent trend/volatility memory, a
plugin loader, visualization, a Flask API - has no `aeon-ai` counterpart.
