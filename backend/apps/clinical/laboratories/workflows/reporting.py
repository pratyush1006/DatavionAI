from django.utils import timezone

from ..models import LaboratoryReport
from ..workflow_registry import REPORT_TRANSITIONS
from .engine import transition


def transition_report(
    *, report_id, organization_id, target_state, actor_id=None, reason=""
):
    report = LaboratoryReport.objects.select_for_update().get(
        id=report_id,
        organization_id=organization_id,
        is_deleted=False,
    )

    def guard(current, target):
        target_value = str(getattr(target, "value", target))
        if target_value in {"final", "amended"} and not report.report_data:
            raise ValueError("Final or amended laboratory report requires report data.")

    def sync(state):
        report.status = state
        if str(getattr(state, "value", state)) in {"final", "amended"}:
            report.released_at = timezone.now()
        report.save(update_fields=["status", "released_at", "updated_at"])

    return transition(
        organization_id=organization_id,
        workflow="report",
        entity_type="LaboratoryReport",
        entity_id=report.id,
        target_state=target_state,
        graph=REPORT_TRANSITIONS,
        actor_id=actor_id,
        reason=reason,
        state_model=report.status,
        guard=guard,
        sync=sync,
    )
