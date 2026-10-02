from apps.imaging.constants.choices import (
    ImagingOrderStatus,
    ImagingReportStatus,
    ImagingStudyStatus,
)
from apps.imaging.workflows.order import transition_order
from apps.imaging.workflows.reporting import transition_report
from apps.imaging.workflows.study import transition_study


def mark_order_ready(*, order_id, tenant_id, actor_id=None):
    return transition_order(
        order_id=order_id,
        tenant_id=tenant_id,
        target_state=ImagingOrderStatus.READY,
        actor_id=actor_id,
    )


def schedule_order(*, order_id, tenant_id, actor_id=None):
    return transition_order(
        order_id=order_id,
        tenant_id=tenant_id,
        target_state=ImagingOrderStatus.SCHEDULED,
        actor_id=actor_id,
    )


def start_order(*, order_id, tenant_id, actor_id=None):
    return transition_order(
        order_id=order_id,
        tenant_id=tenant_id,
        target_state=ImagingOrderStatus.IN_PROGRESS,
        actor_id=actor_id,
    )


def complete_order(*, order_id, tenant_id, actor_id=None):
    return transition_order(
        order_id=order_id,
        tenant_id=tenant_id,
        target_state=ImagingOrderStatus.COMPLETED,
        actor_id=actor_id,
    )


def cancel_order_workflow(*, order_id, tenant_id, reason, actor_id=None):
    return transition_order(
        order_id=order_id,
        tenant_id=tenant_id,
        target_state=ImagingOrderStatus.CANCELLED,
        actor_id=actor_id,
        reason=reason,
    )


def mark_study_arrived(*, study_id, tenant_id, actor_id=None):
    return transition_study(
        study_id=study_id,
        tenant_id=tenant_id,
        target_state=ImagingStudyStatus.ARRIVED,
        actor_id=actor_id,
    )


def mark_study_ready(*, study_id, tenant_id, actor_id=None):
    return transition_study(
        study_id=study_id,
        tenant_id=tenant_id,
        target_state=ImagingStudyStatus.READY,
        actor_id=actor_id,
    )


def start_study(*, study_id, tenant_id, actor_id=None):
    return transition_study(
        study_id=study_id,
        tenant_id=tenant_id,
        target_state=ImagingStudyStatus.ACQUIRING,
        actor_id=actor_id,
    )


def complete_acquisition(*, study_id, tenant_id, acquired_by_id=None, actor_id=None):
    from django.utils import timezone

    from apps.imaging.models import ImagingStudy

    state = transition_study(
        study_id=study_id,
        tenant_id=tenant_id,
        target_state=ImagingStudyStatus.ACQUIRED,
        actor_id=actor_id,
    )
    if acquired_by_id is not None:
        study = ImagingStudy.objects.get(id=study_id, tenant_id=tenant_id)
        study.performed_at = timezone.now()
        study.acquired_by_id = acquired_by_id
        study.save(update_fields=["performed_at", "acquired_by_id", "updated_at"])
    return state


def move_to_interpretation(*, study_id, tenant_id, actor_id=None):
    return transition_study(
        study_id=study_id,
        tenant_id=tenant_id,
        target_state=ImagingStudyStatus.PRELIMINARY,
        actor_id=actor_id,
    )


def finalize_report(*, report_id, tenant_id, radiologist_id):
    return transition_report(
        report_id=report_id,
        tenant_id=tenant_id,
        target_state=ImagingReportStatus.FINAL,
        radiologist_id=radiologist_id,
    )
