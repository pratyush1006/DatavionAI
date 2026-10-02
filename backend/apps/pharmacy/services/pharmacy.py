from apps.pharmacy.models import Pharmacy


def create_pharmacy(*, organization, data, actor=None):
    return Pharmacy.objects.create(organization=organization, **data)
