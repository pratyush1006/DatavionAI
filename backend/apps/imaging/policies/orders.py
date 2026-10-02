def can_transition_order(*, current, target):
    from apps.imaging.workflow_registry import can_transition

    return can_transition("order", current, target)
