from aeon_trikaya import AeonTrikayaSystem
from aeon_trikaya.trikaya import trikaya_state


def test_diamond_interface():
    system = AeonTrikayaSystem(depth=3)
    result = system.run_cycle(input_values=[0.1, 0.2, 0.3])
    assert isinstance(result, dict)
    assert "crep_score" in result

    crep = system.get_crep_state()
    assert all(k in crep for k in ["C", "R", "E", "P", "Gamma"])
    assert all(0.0 <= crep[k] <= 1.0 for k in ["C", "R", "E", "P"])

    utac = system.get_utac_state()
    assert all(k in utac for k in ["H", "H_star", "K_eff"])
    assert utac["K_eff"] > 0.0

    assert isinstance(system.get_phase_events(), list)
    assert len(system.get_phase_events()) == 1

    zr = system.to_zenodo_record()
    assert all(k in zr for k in ["title", "description", "creators"])
    assert "P52" in zr["title"]


def test_diamond_interface_requires_convergence():
    from diamond_setup.protocol import NotConvergedError

    system = AeonTrikayaSystem()
    try:
        system.get_crep_state()
        raise AssertionError("expected NotConvergedError before run_cycle()")
    except NotConvergedError:
        pass


def test_get_trikaya_state_matches_real_function():
    """get_trikaya_state() must return exactly what trikaya.trikaya_state()
    would for the resulting crep_score - no independently-invented enum."""
    system = AeonTrikayaSystem(depth=1)
    result = system.run_cycle(input_values=[100.0, 100.0, 100.0])
    assert system.get_trikaya_state() == trikaya_state(result["crep_score"])


def test_multiple_cycles_accumulate_phase_events():
    system = AeonTrikayaSystem(depth=1)
    system.run_cycle(input_values=[0.1])
    system.run_cycle(input_values=[0.9])
    assert len(system.get_phase_events()) == 2
