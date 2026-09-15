# Contributing

Thanks for your interest in contributing to this GenesisAeon ecosystem
package!

## Getting started

1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
   (or `.venv\Scripts\activate` on Windows).
3. Install in editable mode with dev dependencies: `pip install -e ".[dev]"`.
4. Run the test suite: `pytest`.

## Code style

- Format with `ruff format` and lint with `ruff check`.
- Type-check with `mypy` (this package uses `mypy --strict`).
- Keep functions documented with docstrings where the behavior isn't
  obvious from the name and signature.

## Diamond Interface

This package implements the GenesisAeon Diamond Interface (`run_cycle`,
`get_crep_state`, `get_utac_state`, `get_phase_events`,
`to_zenodo_record`). Any change to these methods' signatures or return
shapes is a **breaking change** and requires a MAJOR version bump (see
`RELEASE_GUIDE.md`).

## Pull requests

- One logical change per PR.
- Add or update tests for any behavioral change.
- Update `CHANGELOG.md` under an `## [Unreleased]` section.
- Fill out the PR template (`.github/PULL_REQUEST_TEMPLATE.md`).

## Reporting issues

Please use the issue templates in `.github/ISSUE_TEMPLATE/` — they help us
triage bug reports vs. feature requests quickly.

## Scientific claims

This is an active research package. `epistemic_status.md` tracks which
parts are real/working vs. speculative or stubbed (e.g. `crep_eval.py`'s
`evaluate_crep()` is a non-functional stub kept for API compatibility).
If your contribution touches any claim about CREP/Trikaya behavior,
please keep that document accurate and clearly mark speculative vs.
validated claims.
