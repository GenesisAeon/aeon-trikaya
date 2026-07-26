# Epistemic Status — aeon-trikaya (P52)

Status: EXPLORATORY — Pre-Alpha, ported real code + honestly-scoped Diamond wrapper.

## What this package actually is (vs. the aspirational vision)

`unified-mandala/GenesisAeonAdvancedAi/` describes an ambitious "AeonNeuroNetz"
architecture (see `docs/blueprints/`): a PyTorch/TensorFlow neural core,
"AeonMembraneLayers" doing bidirectional numeric<->symbolic translation, a
Mandala-UI, a VR platform, and a roster of specialised agents (CoreAgent,
MembraneAgent, VisualAgent, SoundAgent, SymbolAgent, CI/CDAgent, DockerAgent),
with milestones through Q2 2027.

**None of that exists in code.** What is actually implemented, read in full
before writing anything here, is a much more modest but genuinely
functional rule-based pipeline:

1. Numeric values -> "symbolic" representation: tone frequencies (`sonify`),
   HSL colors (`visualize_light`), a single glyph chosen by average value
   or an `archetypes.yaml`-configured context (`assign_symbol`).
2. A discrete CREP score in `{-1, 0, 1}` from average tone frequency
   (`CREP_eval`) plus richer (but unbounded, not normalised) coherence/
   resonance/emergence/presence metrics from variance, cross-correlation,
   and mean absolute step change (`advanced_crep_eval`).
3. A Trikaya state lookup (`trikaya_state`): exactly `{1: PRÄSENZ, 0: LEERE,
   -1: AUFLÖSUNG}`, else `UNBEKANNT`. This is a **discrete** lookup table,
   not a continuous H > H* comparison - see the correction below.
4. An optional fractal refeedback loop (`fraktal_feedback*`): if the score
   is -1, invert the tone frequencies and retry, up to `depth` times.
5. Deterministic haiku/poetry generation keyed off the assigned symbol
   or metric average - three-line poems, not generative/ML text.
6. Persistent JSON memory (`memory_store`) with mean/median/trend/
   volatility analytics across stored cycles.
7. A CLI (`aeon_cli`) wiring all of the above together, plus a second,
   independent agent variant (`advanced_agent`) with YAML-based
   persistence, and a minimal Flask API (`aeon_web`) exposing `/aeon/act`
   and `/aeon/summary`.

This is a genuine, working precursor to "AeonNeuroNetz" - not the neural
architecture itself, but the symbolic/CREP/Trikaya scaffolding one layer
of it would eventually plug into.

## Correction vs. the original extraction prompt

The prompt proposing this extraction described `TrikayaState` as a
continuous classification (`PRÄSENZ -> H > H*`, `LEERE -> H ≈ H*`,
`AUFLÖSUNG -> H < H*`) with lowercase enum values. The real,
already-shipped `trikaya.py` and its own documentation (`Trikaya.md`,
ported verbatim to `docs/blueprints/`) are unambiguous: it is a **discrete**
lookup over exactly `{-1, 0, 1}`, uppercase strings, with a fourth
`UNBEKANNT` case for anything else - there is no continuous H/H*
threshold anywhere in the code. `AeonTrikayaSystem.get_trikaya_state()`
returns the real function's actual output rather than introducing a new,
differently-cased enum that would silently diverge from it.

## CREP terminology note: "P" means Presence here, not Poetics

`aeon-ai`'s `CREPEvaluator` defines C-R-E-P as Coherence-Resonance-
Emergence-**Poetics**. This package's own concept paper
(`docs/blueprints/AeonNeurNetzKonzeptPapier.md`, section 2.3) and its
actual code (`crep_eval.py`'s keys, `aeon_processor.advanced_crep_eval`'s
`"präsenz"` key) define it as Coherence-Resonance-Emergence-**Presence**.
Both are legitimate, independently-documented uses of the same acronym
within the GenesisAeon ecosystem - not a bug, but worth knowing before
assuming "P" means the same thing in every Diamond-interface package.

## Known non-functional stub: `crep_eval.py`

`crep_eval.evaluate_crep()` returns hardcoded static values
(`{"coherence": 0.85, "resonance": 0.75, "emergence": 0.65, "presence": 1.0}`)
regardless of input - it does not compute anything from its argument.
Ported faithfully (it is part of the original public API, re-exported
from `__init__.py`) but flagged here explicitly: do not treat its output
as real. The genuinely functional CREP logic is `aeon_processor.CREP_eval`
and `aeon_processor.advanced_crep_eval`, used throughout the rest of the
pipeline. Similarly, `AdvancedAeonAgent.crep_reflection()` in
`advanced_agent.py` also returns hardcoded values - the same caveat applies.

## Files intentionally left behind (not ported)

`ToDo.yaml`, `codexwork.yaml`, `feedback.json`, `aeon_ui.html` - grepped
the whole module tree, none of these are read by any Python code. They
are stray artifacts (a to-do tracker, a governance file, likely a JSON
duplicate of `feedback.md`, and a static HTML page not served by
`aeon_web.py`'s Flask app, which only returns JSON). Left in
`unified-mandala` rather than carried forward as dead weight.

## Diamond Interface mapping (honest, not fabricated)

- `get_crep_state()`: uses `advanced_crep_eval`'s real per-cycle metrics
  (coherence/resonance/emergence/presence), clamped to `[0,1]` for
  Pydantic's `CREPState` - these are unbounded quantities (variance,
  correlation, mean absolute step change) with no principled [0,1] scale
  from a single cycle, so clamping (not renormalising against history) is
  the honest choice here.
- `get_utac_state()`: `H` is the discrete crep_score (-1/0/1) linearly
  mapped to `[0,1]`; `H_star = 0.5` is the LEERE midpoint; `K_eff` is the
  fractal feedback depth used.
- `get_phase_events()`: the agent's own memory history, one event per
  past cycle with its Trikaya state and chosen action.
- `to_zenodo_record()`: title contains "P52" per ecosystem convention.

## Verbindung zum Ökosystem

- `aeon-ai`: diffed directly (see `unified-mandala/MANDALA_MAP.md`,
  2026-07-26) - real but modest overlap (~20% of modules), this package's
  ~80% (trikaya, fractal feedback, memory store, plugin loader,
  visualization, Flask API) has no `aeon-ai` counterpart at all.
- `scope-resilience` (P41), `genesis-mssc` (P49): mentioned as possible
  future connections in the original extraction prompt (Ρ_sem, somatic
  states) - not investigated, not implemented, flagged as unverified
  rather than assumed.

## What was NOT done in this sprint

No implementation of the Q2-2027 blueprint milestones (neural core, VR,
Mandala-UI, the full agent roster). Only: port the real, already-working
code faithfully, wrap it in the Diamond Interface, document the gap
between vision and implementation honestly, tag Pre-Alpha.
