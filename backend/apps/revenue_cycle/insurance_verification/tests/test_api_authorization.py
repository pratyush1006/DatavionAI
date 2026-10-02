from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.revenue_cycle.insurance_verification.api.views.insurance_verification import (
    InsuranceVerificationListCreateAPIView,
)


class InsuranceVerificationAuthorizationTests(SimpleTestCase):
    def test_denied_list_permission_stops_before_selector(self):
        tenant_id = uuid4()
        request = APIRequestFactory().get("/api/insurance-verification/")
        request.tenant = SimpleNamespace(pk=tenant_id)
        request.organization = SimpleNamespace(pk=uuid4(), tenant_id=tenant_id)
        force_authenticate(
            request,
            user=SimpleNamespace(pk=uuid4(), is_authenticated=True, is_active=True),
        )

        with (
            patch(
                "apps.revenue_cycle.insurance_verification.api.views.insurance_verification.can_view",
                return_value=False,
            ),
            patch(
                "apps.revenue_cycle.insurance_verification.api.views.insurance_verification.list_verifications"
            ) as list_verifications,
        ):
            response = InsuranceVerificationListCreateAPIView.as_view()(request)

        self.assertEqual(response.status_code, 403)
        list_verifications.assert_not_called()
