"""The whole point of this package: its processes auto-register into any core.

``allocate_core()`` walks every installed ``bigraph-schema`` dependent and
registers its ``Process`` / ``Step`` subclasses — so simply having
``pbg-basic-processes`` installed must surface Clock / Intervention /
MathExpressionStep in the link registry with no explicit ``register_*`` call,
exactly like ``pbg-emitters``.
"""
from bigraph_schema import allocate_core


def test_processes_auto_register_via_discovery():
    core = allocate_core()
    link_reg = getattr(core, 'link_registry', {}) or {}
    for name in ('Clock', 'Intervention', 'MathExpressionStep'):
        assert name in link_reg, f"{name} was not auto-discovered into the core registry"
