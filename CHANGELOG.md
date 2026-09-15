# Changelog

## [0.1.1] - 2026-07-26

- Fixed (2026-09-15, found by the new CI while setting up this package's
  GitHub repo and release infrastructure): `requires-python = ">=3.10"`
  was wrong -- `diamond-setup>=2.2.0` requires Python >=3.11, so
  installing on 3.10 failed with "No matching distribution found".
  Bumped to `>=3.11` (pyproject.toml, classifiers, ruff/mypy target,
  CI matrix) -- the same chronic Python-3.10-vs-diamond-setup mismatch
  already found and fixed in `neural-avalanche-utac`. Also fixed CI/
  release workflows installing only `.[dev]`, which doesn't pull in the
  `flask`/`plotly` extras that `test_aeon_web.py`,
  `test_feedback_graph.py`, and `test_mandala_visualizer.py` import
  unconditionally -- passed locally only because both were already
  installed globally on the dev machine. Now installs `.[dev,plotting,flask]`.
- Fixed: `import aeon_trikaya` crashed with `ModuleNotFoundError: No module
  named 'plotly'` unless the optional `[plotting]` extra was also
  installed, because `__init__.py` unconditionally imported
  `plot_crep_mandala` (which needs plotly) at module load time - found
  while building `aeon-sealcore` (P54), which depends on this package
  without needing plotting. `plot_crep_mandala` is now imported inside a
  try/except and only added to `__all__` when plotly is actually
  installed; `from aeon_trikaya import plot_crep_mandala` now fails with
  a normal `ImportError` (not a crash on unrelated imports) if `[plotting]`
  wasn't installed.

## [0.1.0] - 2026-07-26

- Extracted from `unified-mandala/GenesisAeonAdvancedAi/`: 17 real, working
  modules ported faithfully (numeric-to-symbolic translation, discrete CREP
  scoring, Trikaya state classification, fractal refeedback, persistent
  trend/volatility memory, plugin manifest loader, feedback-graph and
  mandala visualization, a CLI, a minimal Flask API). All 20 original test
  files ported and passing under the new package name.
- `AeonTrikayaSystem`: full six-method Diamond Interface implementation
  (GenesisAeon Package 52), plus `get_trikaya_state()`.
- `docs/blueprints/`: the 9 original blueprint/concept documents carried
  forward as documentation (not packaged into the wheel) - describe a much
  larger "AeonNeuroNetz" vision (neural core, VR, Mandala-UI) with
  milestones through Q2 2027, none of which exists in code yet.
- Corrected two claims from the original extraction prompt (see
  `epistemic_status.md`): Trikaya is a discrete lookup over `{-1,0,1}`,
  not a continuous H > H* threshold; `crep_eval.py`'s `evaluate_crep()` is
  a non-functional stub returning hardcoded values, kept for API
  compatibility but flagged explicitly.
- Not on PyPI yet - Pre-Alpha, active research package.
