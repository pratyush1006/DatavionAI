from django.db import transaction

from apps.imaging.models import RadiologyReportVersion


@transaction.atomic
def create_report_version(*, report, authored_by_id, reason=""):
    next_version = (
        RadiologyReportVersion.objects.filter(
            tenant_id=report.tenant_id, report=report
        ).count()
        + 1
    )
    return RadiologyReportVersion.objects.create(
        tenant_id=report.tenant_id,
        report=report,
        version=next_version,
        status=report.status,
        findings_text=report.findings_text,
        impression=report.impression,
        authored_by_id=authored_by_id,
        created_reason=reason,
    )
