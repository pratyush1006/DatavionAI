from apps.imaging.models import ImagingOrder, ImagingStudy, RadiologyReport


def orders_for_tenant(tenant_id):
    return ImagingOrder.objects.filter(tenant_id=tenant_id)


def studies_for_tenant(tenant_id):
    return ImagingStudy.objects.select_related("order", "procedure").filter(
        tenant_id=tenant_id
    )


def reports_for_tenant(tenant_id):
    return RadiologyReport.objects.select_related("study").filter(tenant_id=tenant_id)
