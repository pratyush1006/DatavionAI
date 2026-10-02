from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

ORDER_TRANSITIONS = MappingProxyType(
    {
        "draft": frozenset({"ordered", "cancelled"}),
        "ordered": frozenset({"ready", "cancelled"}),
        "ready": frozenset({"scheduled", "cancelled"}),
        "scheduled": frozenset({"in_progress", "cancelled"}),
        "in_progress": frozenset({"completed", "cancelled"}),
        "completed": frozenset(),
        "cancelled": frozenset(),
    }
)

STUDY_TRANSITIONS = MappingProxyType(
    {
        "scheduled": frozenset({"arrived", "ready", "acquiring", "cancelled"}),
        "arrived": frozenset({"ready", "cancelled"}),
        "ready": frozenset({"acquiring", "cancelled"}),
        "acquiring": frozenset({"acquired", "cancelled"}),
        "acquired": frozenset({"preliminary", "final", "cancelled"}),
        "preliminary": frozenset({"final", "amended", "cancelled"}),
        "final": frozenset({"amended"}),
        "amended": frozenset({"final"}),
        "cancelled": frozenset(),
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


def allowed_transitions(
    graph: Mapping[str, frozenset[str]], state: str
) -> frozenset[str]:
    return graph.get(state, frozenset())


def assert_transition(
    graph: Mapping[str, frozenset[str]], current: str, target: str
) -> None:
    if target not in allowed_transitions(graph, current):
        raise ValueError(
            f"Illegal Imaging workflow transition: {current!r} -> {target!r}"
        )
