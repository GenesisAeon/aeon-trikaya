"""aeon-trikaya — rule-based numeric-to-symbolic sensemaking with fractal
CREP feedback and Trikaya state classification (GenesisAeon P52).

Ported from unified-mandala/GenesisAeonAdvancedAi/. See epistemic_status.md
for what this package actually implements vs. the much larger aspirational
"AeonNeuroNetz" vision (PyTorch/TensorFlow neural core, VR/Mandala-UI,
CI/CD/Docker/Visual/Sound/Symbol agents) described in docs/blueprints/ -
none of that exists in code; this package is the working, non-ML
precursor: numeric -> symbol (tone/color/glyph) -> discrete CREP score
-> Trikaya state -> optional fractal refeedback -> persistent memory.
"""

__version__ = "0.1.1"

from .adaptive_threshold import auto_adapt_crep_threshold
from .advanced_agent import AdvancedAeonAgent
from .aeon_agent import AeonAgent
from .aeon_logger import log_event
from .aeon_processor import symbolic_manifestation
from .archetype_tools import get_symbol
from .crep_eval import evaluate_crep
from .memory_store import (
    load_results,
    store_result,
    summarize_entries,
    summarize_memory,
    summarize_stats,
    summarize_stats_memory,
    tail_results,
    trend_metric,
    volatility_metric,
    volatility_metric_memory,
)
from .plugin_loader import load_plugin_manifest, load_plugins
from .symbol_tools import assign_color, transform_to_symbol
from .system import AeonTrikayaSystem

# plot_crep_mandala needs plotly, only installed via the optional
# `plotting` extra - importing it unconditionally here would make that
# extra not actually optional (see aeon-sealcore's epistemic_status.md,
# which caught this while depending on this package without [plotting]).
try:
    from .mandala_visualizer import plot_crep_mandala  # noqa: F401 (re-exported below)

    _HAS_PLOTTING = True
except ImportError:
    _HAS_PLOTTING = False

__all__ = [
    "AeonAgent",
    "AdvancedAeonAgent",
    "AeonTrikayaSystem",
    "assign_color",
    "transform_to_symbol",
    "evaluate_crep",
    "log_event",
    "symbolic_manifestation",
    "auto_adapt_crep_threshold",
    "load_plugin_manifest",
    "load_plugins",
    "get_symbol",
    "store_result",
    "load_results",
    "summarize_memory",
    "summarize_entries",
    "summarize_stats",
    "summarize_stats_memory",
    "tail_results",
    "trend_metric",
    "volatility_metric",
    "volatility_metric_memory",
]

if _HAS_PLOTTING:
    __all__.append("plot_crep_mandala")

