"""Patient Address querysets and manager."""

from __future__ import annotations

from django.db import models


class AddressQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(status="inactive")

    def for_tenant(self, tenant):
        return self.filter(tenant=tenant)

    def for_organization(self, organization):
        return self.filter(organization=organization)

    def for_patient(self, patient):
        return self.filter(patient=patient)

    def with_relations(self):
        return self.select_related(
            "tenant", "organization", "patient", "country", "region", "city"
        )


class AddressManager(models.Manager.from_queryset(AddressQuerySet)):
    """Canonical Address manager."""
