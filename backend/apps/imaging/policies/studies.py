def can_transition_study(*, current, target):
    from apps.imaging.workflow_registry import can_transition

    return can_transition("study", current, target)
