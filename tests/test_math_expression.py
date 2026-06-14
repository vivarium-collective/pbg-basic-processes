"""Tests for the MathExpressionStep."""
import math

import pytest

from bigraph_schema import allocate_core
from process_bigraph import Composite

from pbg_basic_processes.math_expression import MathExpressionStep


def _step_node(expressions, params=None, inputs=None, outputs=None):
    node = {
        '_type': 'step',
        'address': 'local:MathExpressionStep',
        'config': {'expressions': expressions, 'params': params or {}, 'debug': False},
        'inputs': inputs or {},
        'outputs': outputs or {},
    }
    return node


def _run(state, node, steps=1):
    core = allocate_core()
    state = dict(state)
    state['math'] = node
    comp = Composite({'state': state}, core=core)
    comp.run(steps)
    return comp.state


def test_simple_expression():
    node = _step_node(
        [{'out': 'z', 'expr': 'a + b'}],
        inputs={'a': ['a'], 'b': ['b']},
        outputs={'z': ['z']},
    )
    end = _run({'a': 2.0, 'b': 3.0, 'z': 0.0}, node)
    assert end['z'] == pytest.approx(5.0)


def test_dependency_order_resolved():
    # w depends on z which depends on a,b — listed out of order on purpose.
    node = _step_node(
        [{'out': 'w', 'expr': 'z * 2'}, {'out': 'z', 'expr': 'a + b'}],
        inputs={'a': ['a'], 'b': ['b']},
        outputs={'z': ['z'], 'w': ['w']},
    )
    end = _run({'a': 1.0, 'b': 4.0, 'z': 0.0, 'w': 0.0}, node)
    assert end['z'] == pytest.approx(5.0)
    assert end['w'] == pytest.approx(10.0)


def test_params_are_constants_not_ports():
    step = MathExpressionStep(
        {'expressions': [{'out': 'y', 'expr': 'k * x'}], 'params': {'k': 3.0}, 'debug': False},
        allocate_core(),
    )
    step.initialize()
    assert 'x' in step.inputs()
    assert 'k' not in step.inputs()  # param, not a port
    assert 'y' in step.outputs()


def test_cycle_raises():
    # initialize() runs during construction, so the ValueError surfaces there.
    with pytest.raises(ValueError, match='Cyclic'):
        MathExpressionStep(
            {'expressions': [{'out': 'a', 'expr': 'b'}, {'out': 'b', 'expr': 'a'}], 'debug': False},
            allocate_core(),
        )


def test_empty_expressions_raises():
    with pytest.raises(ValueError, match='non-empty'):
        MathExpressionStep({'expressions': [], 'debug': False}, allocate_core())


def test_nonlinear_with_param():
    node = _step_node(
        [{'out': 'y', 'expr': 'sin(x) + k'}],
        params={'k': 1.0},
        inputs={'x': ['x']},
        outputs={'y': ['y']},
    )
    end = _run({'x': float(math.pi / 2), 'y': 0.0}, node)
    assert end['y'] == pytest.approx(2.0)
