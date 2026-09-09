"""
Runtime contract tests for Patient Referrals.

These tests exercise deterministic workflow-result-to-HTTP behavior and
expected domain-error classification without requiring project-specific
organization fixtures.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

from django.test import SimpleTestCase
from rest_framework import status

from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.patient_management.referrals.api.views.referral import (
    _workflow_response,
)


class PatientReferralRuntimeContractTests(SimpleTestCase):
    """Verify stable API contracts for expected workflow outcomes."""

    def _context(self) -> WorkflowContext:
        """Build a minimal workflow context for result contract tests."""

        return WorkflowContext.create(
            tenant_id="00000000-0000-0000-0000-000000000001",
            actor_id="00000000-0000-0000-0000-000000000002",
            workflow_name="patient_referral.test",
        )

    def test_permission_failure_returns_403(self) -> None:
        """Permission failures must be exposed as HTTP 403."""

        result = WorkflowResult.fail(
            context=self._context(),
            message="Permission denied.",
            code="patient_referral_permission_denied",
        )

        response = _workflow_response(result)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found_failure_returns_404(self) -> None:
        """Missing referrals must be exposed as HTTP 404."""

        result = WorkflowResult.fail(
            context=self._context(),
            message="Patient referral was not found.",
            code="patient_referral_not_found",
        )

        response = _workflow_response(result)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_duplicate_number_returns_409(self) -> None:
        """Duplicate referral numbers must be exposed as HTTP 409."""

        result = WorkflowResult.fail(
            context=self._context(),
            message="A referral with this referral number already exists.",
            code="patient_referral_duplicate_number",
        )

        response = _workflow_response(result)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_unexpected_workflow_failure_returns_500(self) -> None:
        """Unexpected workflow failures must not be reported as client errors."""

        result = WorkflowResult.fail(
            context=self._context(),
            message="Unexpected workflow failure.",
            code="workflow_execution_error",
        )

        response = _workflow_response(result)

        self.assertEqual(
            response.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def test_success_response_preserves_serializer_contract(self) -> None:
        """Successful workflow responses must remain unchanged."""

        serializer = Mock()
        serializer.return_value.data = {"id": "referral"}
        result = WorkflowResult.ok(
            context=self._context(),
            data=SimpleNamespace(id="referral"),
            message="Success.",
            code="patient_referral_updated",
        )

        response = _workflow_response(
            result,
            serializer,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": "referral"})


__all__ = ("PatientReferralRuntimeContractTests",)
