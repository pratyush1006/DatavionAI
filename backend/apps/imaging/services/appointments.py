from apps.imaging.models import ImagingAppointmentLink


def appointment_link(*, tenant_id, order_id):
    return ImagingAppointmentLink.objects.filter(
        tenant_id=tenant_id, order_id=order_id
    ).first()
