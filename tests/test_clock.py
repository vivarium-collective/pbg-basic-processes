"""Tests for the Clock step-counter process."""
import pytest

from bigraph_schema import allocate_core
from process_bigraph import Composite

from pbg_basic_processes.clock import Clock, register_clock, clock_node


def _run(node, run_for):
    core = allocate_core()
    register_clock(core)
    comp = Composite({'state': {'tick': 0, 'clk': node}}, core=core)
    comp.run(run_for)
    return comp.state


def test_register_is_idempotent_and_safe():
    core = allocate_core()
    register_clock(core)
    assert register_clock(core) is False
    assert 'Clock' in (getattr(core, 'link_registry', {}) or {})


def test_tick_counts_updates_at_unit_interval():
    # run for 5 time units at interval 1.0 -> 5 updates
    end = _run(clock_node(interval=1.0), run_for=5)
    assert end['tick'] == 5


def test_tick_counts_finer_steps():
    # run for 4 time units at interval 0.25 -> 16 updates
    end = _run(clock_node(interval=0.25), run_for=4)
    assert end['tick'] == 16


def test_start_tick_offset_applied():
    end = _run(clock_node(start_tick=100, interval=1.0), run_for=3)
    assert end['tick'] == 103


def test_does_not_touch_reserved_global_time():
    # Clock must NOT corrupt the engine's master clock: global_time still equals
    # the run duration even with the clock present.
    end = _run(clock_node(interval=1.0), run_for=4)
    assert end['global_time'] == pytest.approx(4.0)


def test_clock_node_shape():
    n = clock_node(tick_path=['n'])
    assert n['_type'] == 'process'
    assert n['address'] == 'local:Clock'
    assert n['inputs'] == {}
    assert n['outputs']['tick'] == ['n']
    assert 'global_time' not in n['outputs']


def test_clock_takes_no_inputs():
    clk = Clock({}, allocate_core())
    assert clk.inputs() == {}
    assert set(clk.outputs().keys()) == {'tick'}
