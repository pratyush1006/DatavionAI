"""Architecture tests for Revenue Cycle cross-module integration."""

from __future__ import annotations

from django.test import SimpleTestCase

from ..models import RevenueCycleIntegrationRecord


class CrossModuleIntegrationArchitectureTests(SimpleTestCase):
    """Verify non-negotiable integration architecture."""

    def test_organization_scope_exists(self) -> None:
        """Verify integration records are organization scoped."""

        field = RevenueCycleIntegrationRecord._meta.get_field("organization")
        self.assertIsNotNone(field.remote_field.model)

    def test_idempotency_constraint_exists(self) -> None:
        """Verify organization-scoped idempotency is enforced."""

        constraint_names = {
            constraint.name
            for constraint in RevenueCycleIntegrationRecord._meta.constraints
        }
        self.assertIn(
            "unique_rc_integration_idempotency",
            constraint_names,
        )

    def test_processing_state_exists(self) -> None:
        """Verify integration processing has explicit lifecycle states."""

        field = RevenueCycleIntegrationRecord._meta.get_field("status")
        self.assertEqual(field.default, "PENDING")


__all__ = ("CrossModuleIntegrationArchitectureTests",)
