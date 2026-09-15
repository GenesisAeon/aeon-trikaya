# Release Guide

This package follows the GenesisAeon ecosystem release process.

## Versioning

We use [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

- **MAJOR** — breaking changes to the public API or Diamond Interface
  (`run_cycle`, `get_crep_state`, `get_utac_state`, `get_phase_events`,
  `to_zenodo_record`).
- **MINOR** — new features, backwards-compatible.
- **PATCH** — bug fixes, documentation, dependency bumps.

## Before the first PyPI release

This package is not on PyPI yet (Pre-Alpha). Before tagging a release:

1. Register the `aeon-trikaya` project name on PyPI (either by a first
   manual `twine upload` or by creating the project via the PyPI web UI).
2. Add a `PYPI_API_TOKEN` repository secret at
   `Settings -> Secrets and variables -> Actions` with a PyPI API token
   scoped to this project.
3. Optionally enable Zenodo-GitHub integration at
   https://zenodo.org/account/settings/github/ so GitHub Releases mint a
   Zenodo DOI automatically using `.zenodo.json`.

## How to cut a release

1. Ensure `CHANGELOG.md` has an entry for the new version under
   `## [X.Y.Z]`.
2. Ensure `pyproject.toml`'s `[project].version`, `CITATION.cff`'s
   `version`, and `.zenodo.json`'s `"version"` all match.
3. Commit these changes to `main`.
4. Tag: `git tag vX.Y.Z && git push origin vX.Y.Z`.
5. The `.github/workflows/release.yml` workflow builds, tests, and
   publishes to PyPI + creates a GitHub Release automatically.
6. If Zenodo-GitHub integration is enabled, a new Zenodo DOI version is
   minted automatically from the GitHub Release.

## Dependency pins within the GenesisAeon ecosystem

If this package depends on other `GenesisAeon/*` packages, pin them with
`>=` lower bounds matching the minimum version that provides the API this
package relies on. Do not pin exact versions (`==`) for ecosystem
dependencies.
