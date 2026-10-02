from __future__ import annotations

from django.utils import timezone

from apps.imaging.constants.choices import ImagingReportStatus, ImagingStudyStatus
from apps.imaging.models import RadiologyReport
from apps.imaging.workflow_registry import REPORT_TRANSITIONS
from apps.imaging.workflows.engine import transition


def transition_report(
    *, report_id, tenant_id, target_state, radiologist_id=None, reason=""
):
    report = (
        RadiologyReport.objects.select_for_update()
        .select_related("study")
        .get(id=report_id, tenant_id=tenant_id)
    )
    if (
        target_state in {ImagingReportStatus.FINAL, ImagingReportStatus.AMENDED}
        and not report.impression.strip()
    ):
        raise ValueError("Final or amended report requires an impression.")

    def sync(state):
        report.status = state
        if state in {ImagingReportStatus.FINAL, ImagingReportStatus.AMENDED}:
            if radiologist_id is not None:
                report.radiologist_id = radiologist_id
            report.signed_at = timezone.now()
            report.save(
                update_fields=["status", "radiologist_id", "signed_at", "updated_at"]
            )
        else:
            report.save(update_fields=["status", "updated_at"])
        if state == ImagingReportStatus.FINAL:
            report.study.status = ImagingStudyStatus.FINAL
            report.study.save(update_fields=["status", "updated_at"])

    return transition(
        tenant_id=tenant_id,
        entity_type="RadiologyReport",
        entity_id=report.id,
        target_state=target_state,
        graph=REPORT_TRANSITIONS,
        actor_id=radiologist_id,
        reason=reason,
        state_model=report.status,
        sync=sync,
    )
