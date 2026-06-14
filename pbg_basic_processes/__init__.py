"""pbg-basic-processes: reusable, composite-agnostic process-bigraph processes.

These processes auto-register into any workspace ``core`` via bigraph-schema
package discovery (``allocate_core`` walks every installed ``bigraph-schema``
dependent and registers its ``Process`` / ``Step`` subclasses) — no entry
points or ``register_*`` boilerplate required. Add ``pbg-basic-processes`` as a
dependency and ``Clock`` / ``Intervention`` / ``MathExpressionStep`` appear in
the registry, the same way ``pbg-emitters`` surfaces its emitters.
"""

from pbg_basic_processes.clock import Clock, register_clock, clock_node
from pbg_basic_processes.intervention import (
    Intervention,
    register_intervention,
    intervention_node,
)

try:
    from pbg_basic_processes.math_expression import MathExpressionStep
except ImportError:  # pragma: no cover - sympy is a base dep, but stay defensive
    pass

__all__ = [
    "Clock",
    "register_clock",
    "clock_node",
    "Intervention",
    "register_intervention",
    "intervention_node",
    "MathExpressionStep",
]
