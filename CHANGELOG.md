# Changelog

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
