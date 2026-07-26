"""AeonTrikayaSystem — Diamond-interface wrapper around AeonAgent (GenesisAeon P52).

Note on TrikayaState: the original extraction prompt proposed a new
`TrikayaState(StrEnum)` with lowercase values ("präsenz"/"leere"/
"auflösung") mapped from a continuous H > H* comparison. The real,
already-implemented `trikaya.trikaya_state()` is a discrete lookup over
exactly {1, 0, -1} (uppercase "PRÄSENZ"/"LEERE"/"AUFLÖSUNG", plus
"UNBEKANNT" for anything else) - there is no continuous H/H* comparison
anywhere in the ported code, and `Trikaya.md` (the real, accurate
documentation) confirms the discrete mapping. `get_trikaya_state()` below
returns the real function's actual string output rather than introducing
a new, differently-cased enum that would silently diverge from it.
"""

from __future__ import annotations

from typing import Any

from diamond_setup.protocol import CREPState, DiamondPackage, UTACState, ZenodoCreator, ZenodoRecord

from .aeon_agent import AeonAgent


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


class AeonTrikayaSystem(DiamondPackage):  # type: ignore[misc]  # diamond-setup ships no py.typed marker
    """GenesisAeon Package 52: numeric -> symbolic -> CREP -> Trikaya pipeline."""

    PACKAGE_ID: int = 52

    def __init__(self, depth: int = 3) -> None:
        super().__init__()
        self.depth = depth
        self._agent = AeonAgent()
        self.input_values: list[float] = []
        self._last_record: dict[str, Any] | None = None

    def run_cycle(self, input_values: list[float] | None = None) -> dict[str, Any]:
        """Execute one numeric -> symbolic -> Trikaya cycle (optional input override)."""
        if input_values is not None:
            self.input_values = input_values
        return super().run_cycle()  # type: ignore[no-any-return]  # same untyped base as above

    def _run_cycle(self) -> dict[str, Any]:
        action, record = self._agent.act(self.input_values, depth=self.depth)
        self._last_record = record
        return {"action": action, **record}

    def _build_crep_state(self) -> CREPState:
        # advanced_crep_eval's metrics are unbounded (variance, correlation,
        # mean-abs-diff), unlike Pydantic's CREPState [0,1] fields - clamped
        # here, not renormalised, since there is no principled scale to map
        # them onto without more data than a single cycle provides.
        metrics = (self._last_record or {}).get("metrics", {})
        return CREPState(
            C=_clamp01(metrics.get("kohärenz", 0.0)),
            R=_clamp01(metrics.get("resonanz", 0.0)),
            E=_clamp01(metrics.get("emergenz", 0.0)),
            P=_clamp01(metrics.get("präsenz", 0.0)),
        )

    def _build_utac_state(self) -> UTACState:
        # The discrete crep_score (-1/0/1) normalised to [0,1]; H_star=0.5
        # is the LEERE midpoint between AUFLÖSUNG (0.0) and PRÄSENZ (1.0).
        score = (self._last_record or {}).get("crep_score", 0)
        h = (score + 1) / 2.0
        return UTACState(H=h, H_star=0.5, K_eff=float(self.depth))

    def _build_phase_events(self) -> list[dict[str, Any]]:
        return [
            {"step": i, "trikaya_state": entry.get("trikaya_state"), "action": entry.get("action")}
            for i, entry in enumerate(self._agent.memory)
        ]

    def _build_zenodo_record(self) -> ZenodoRecord:
        return ZenodoRecord(
            title="aeon-trikaya: Fractal CREP Feedback and Trikaya State Classification (P52)",
            description=(
                "Numeric-to-symbolic sensemaking pipeline (tone/color/glyph translation, "
                "discrete CREP scoring, Trikaya state classification, fractal refeedback, "
                "persistent trend/volatility memory) ported from "
                "unified-mandala/GenesisAeonAdvancedAi. Working precursor to the larger "
                "aspirational 'AeonNeuroNetz' vision (see docs/blueprints/) - no neural "
                "network, VR, or Mandala-UI components exist in code."
            ),
            creators=[ZenodoCreator(name="Römer, Johann", affiliation="MOR Research Collective")],
        )

    def get_trikaya_state(self) -> str:
        """Return the real trikaya.trikaya_state() output for the last cycle."""
        if self._last_record is None:
            return "UNBEKANNT"
        return str(self._last_record.get("trikaya_state", "UNBEKANNT"))
