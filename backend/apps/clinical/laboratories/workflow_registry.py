from __future__ import annotations

from types import MappingProxyType

ORDER_TRANSITIONS = MappingProxyType(
    {
        "ordered": frozenset({"scheduled", "collected", "cancelled"}),
        "scheduled": frozenset({"collected", "cancelled"}),
        "collected": frozenset({"processing", "cancelled"}),
        "processing": frozenset({"verified", "cancelled"}),
        "verified": frozenset({"released", "cancelled"}),
        "released": frozenset(),
        "cancelled": frozenset(),
    }
)

SPECIMEN_TRANSITIONS = MappingProxyType(
    {
        "expected": frozenset({"collected", "rejected"}),
        "collected": frozenset({"received", "rejected"}),
        "received": frozenset({"processing", "rejected"}),
        "processing": frozenset({"completed", "rejected"}),
        "completed": frozenset(),
        "rejected": frozenset(),
    }
)

RESULT_TRANSITIONS = MappingProxyType(
    {
        "pending": frozenset({"preliminary"}),
        "preliminary": frozenset({"final", "corrected"}),
        "final": frozenset({"corrected"}),
        "corrected": frozenset({"final"}),
    }
)

REPORT_TRANSITIONS = MappingProxyType(
    {
        "draft": frozenset({"preliminary", "final"}),
        "preliminary": frozenset({"final", "amended"}),
        "final": frozenset({"amended"}),
        "amended": frozenset({"final"}),
    }
)

WORKFLOW_GRAPHS = MappingProxyType(
    {
        "order": ORDER_TRANSITIONS,
        "specimen": SPECIMEN_TRANSITIONS,
        "result": RESULT_TRANSITIONS,
        "report": REPORT_TRANSITIONS,
    }
)

# Backwards-compatible public contract. The four explicit transition maps
# above remain the authoritative workflow definitions.
WORKFLOWS = {
    "order": ORDER_TRANSITIONS,
    "specimen": SPECIMEN_TRANSITIONS,
    "result": RESULT_TRANSITIONS,
    "report": REPORT_TRANSITIONS,
}


def allowed_transitions(graph, state):
    return graph.get(str(getattr(state, "value", state)), frozenset())


def assert_transition(graph, current, target):
    current = str(getattr(current, "value", current))
    target = str(getattr(target, "value", target))
    if target not in allowed_transitions(graph, current):
        raise ValueError(
            f"Illegal Laboratory workflow transition: {current!r} -> {target!r}"
        )
