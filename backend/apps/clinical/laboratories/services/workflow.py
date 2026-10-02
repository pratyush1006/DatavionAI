from ..constants import OrderStatus, ResultStatus, SpecimenStatus
from ..workflows.order import transition_order
from ..workflows.reporting import transition_report
from ..workflows.result import transition_result
from ..workflows.specimen import transition_specimen


def mark_order_scheduled(*, order_id, organization_id, actor_id=None, reason=""):
    return transition_order(
        order_id=order_id,
        organization_id=organization_id,
        target_state=OrderStatus.SCHEDULED,
        actor_id=actor_id,
        reason=reason,
    )


def mark_order_collected(*, order_id, organization_id, actor_id=None, reason=""):
    return transition_order(
        order_id=order_id,
        organization_id=organization_id,
        target_state=OrderStatus.COLLECTED,
        actor_id=actor_id,
        reason=reason,
    )


def mark_order_processing(*, order_id, organization_id, actor_id=None, reason=""):
    return transition_order(
        order_id=order_id,
        organization_id=organization_id,
        target_state=OrderStatus.PROCESSING,
        actor_id=actor_id,
        reason=reason,
    )


def verify_order(*, order_id, organization_id, actor_id=None, reason=""):
    return transition_order(
        order_id=order_id,
        organization_id=organization_id,
        target_state=OrderStatus.VERIFIED,
        actor_id=actor_id,
        reason=reason,
    )


def release_order(*, order_id, organization_id, actor_id=None, reason=""):
    return transition_order(
        order_id=order_id,
        organization_id=organization_id,
        target_state=OrderStatus.RELEASED,
        actor_id=actor_id,
        reason=reason,
    )


def cancel_order(*, order_id, organization_id, actor_id=None, reason=""):
    return transition_order(
        order_id=order_id,
        organization_id=organization_id,
        target_state=OrderStatus.CANCELLED,
        actor_id=actor_id,
        reason=reason,
    )


def receive_specimen_workflow(
    *, specimen_id, organization_id, actor_id=None, reason=""
):
    return transition_specimen(
        specimen_id=specimen_id,
        organization_id=organization_id,
        target_state=SpecimenStatus.RECEIVED,
        actor_id=actor_id,
        reason=reason,
    )


def start_specimen_processing(
    *, specimen_id, organization_id, actor_id=None, reason=""
):
    return transition_specimen(
        specimen_id=specimen_id,
        organization_id=organization_id,
        target_state=SpecimenStatus.PROCESSING,
        actor_id=actor_id,
        reason=reason,
    )


def complete_specimen_processing(
    *, specimen_id, organization_id, actor_id=None, reason=""
):
    return transition_specimen(
        specimen_id=specimen_id,
        organization_id=organization_id,
        target_state=SpecimenStatus.COMPLETED,
        actor_id=actor_id,
        reason=reason,
    )


def reject_specimen_workflow(*, specimen_id, organization_id, actor_id=None, reason=""):
    return transition_specimen(
        specimen_id=specimen_id,
        organization_id=organization_id,
        target_state=SpecimenStatus.REJECTED,
        actor_id=actor_id,
        reason=reason,
    )


def finalize_result(*, result_id, organization_id, actor_id=None, reason=""):
    return transition_result(
        result_id=result_id,
        organization_id=organization_id,
        target_state=ResultStatus.FINAL,
        actor_id=actor_id,
        reason=reason,
    )


def correct_result(*, result_id, organization_id, actor_id=None, reason=""):
    return transition_result(
        result_id=result_id,
        organization_id=organization_id,
        target_state=ResultStatus.CORRECTED,
        actor_id=actor_id,
        reason=reason,
    )


def finalize_report(*, report_id, organization_id, actor_id=None, reason=""):
    return transition_report(
        report_id=report_id,
        organization_id=organization_id,
        target_state="final",
        actor_id=actor_id,
        reason=reason,
    )


def amend_report(*, report_id, organization_id, actor_id=None, reason=""):
    return transition_report(
        report_id=report_id,
        organization_id=organization_id,
        target_state="amended",
        actor_id=actor_id,
        reason=reason,
    )
