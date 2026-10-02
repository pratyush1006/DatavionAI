from apps.imaging.models import ImagingProcedure


def active_procedures(*, tenant_id):
    return ImagingProcedure.objects.filter(tenant_id=tenant_id, active=True).order_by(
        "procedure_code"
    )
