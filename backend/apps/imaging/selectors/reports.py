from apps.imaging.models import RadiologyReport


def get_report(*, tenant_id, report_id):
    return RadiologyReport.objects.select_related("study").get(
        tenant_id=tenant_id, id=report_id
    )
