from apps.organizations.models import Organization


def create_organization(validated_data):
    """
    Create a new organization.
    """

    organization = Organization.objects.create(
        **validated_data
    )

    return organization


def update_organization(
    organization,
    validated_data,
):
    """
    Update an existing organization.
    """

    for field, value in validated_data.items():
        setattr(
            organization,
            field,
            value,
        )

    organization.save()

    return organization


def delete_organization(
    organization,
):
    """
    Delete an organization.
    """

    organization.delete()