"""Authenticated DatavionOS organization workspace bootstrap API tests."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from rest_framework.test import APIRequestFactory, force_authenticate

from apps.datavionos.api.views.bootstrap import PlatformBootstrapAPIView


class OrganizationWorkspaceBootstrapAPIRuntimeTests(TestCase):
    """Protect the canonical authenticated bootstrap API boundary."""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = SimpleNamespace(
            id="workspace-api-user",
            pk="workspace-api-user",
            is_authenticated=True,
        )
        self.context = SimpleNamespace(
            tenant="workspace-tenant",
            organization="workspace-organization",
            permissions={"workspace.view"},
        )
        self.result = SimpleNamespace(
            modules=("module-a",),
            navigation=("navigation-a",),
            dashboard=("dashboard-a",),
            branding={"name": "DatavionOS"},
            feature_flags={"module-a": True},
            capabilities={"capabilities": {"module-a": True}},
        )
        self.bootstrap = SimpleNamespace(
            context=self.context,
            modules=("module-a",),
            navigation=("navigation-a",),
            dashboard=("dashboard-a",),
        )

    def test_unauthenticated_request_is_rejected(self):
        request = self.factory.get("/api/bootstrap/")
        response = PlatformBootstrapAPIView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    @patch("apps.datavionos.api.views.bootstrap.PlatformBootstrapSerializer")
    @patch("apps.datavionos.api.views.bootstrap.platform_bootstrap_builder")
    @patch("apps.datavionos.api.views.bootstrap.PlatformBootstrapService")
    @patch("apps.datavionos.api.views.bootstrap.platform_bootstrap_selector")
    def test_authenticated_request_uses_canonical_runtime_pipeline(
        self,
        selector,
        service_class,
        builder,
        serializer_class,
    ):
        selector.get.return_value = self.context
        service_class.return_value.bootstrap.return_value = self.result
        builder.build.return_value = self.bootstrap
        serializer_class.return_value.data = {
            "organization": {"id": "workspace-organization"},
            "modules": [{"identifier": "module-a"}],
            "navigation": [{"route": "/module-a"}],
            "dashboard": [{"route": "/module-a"}],
        }

        request = self.factory.get("/api/bootstrap/")
        force_authenticate(request, user=self.user)
        response = PlatformBootstrapAPIView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        selector.get.assert_called_once_with(user=self.user)
        service_class.assert_called_once_with()
        service_class.return_value.bootstrap.assert_called_once_with(
            tenant=self.context.tenant,
            user=self.user,
            organization=self.context.organization,
            permissions=self.context.permissions,
        )
        builder.build.assert_called_once()
        serializer_class.assert_called_once_with(self.bootstrap)
        self.assertEqual(response.data["data"]["modules"][0]["identifier"], "module-a")

    @patch("apps.datavionos.api.views.bootstrap.PlatformBootstrapService")
    @patch("apps.datavionos.api.views.bootstrap.platform_bootstrap_selector")
    def test_runtime_context_is_organization_scoped(self, selector, service_class):
        selector.get.return_value = self.context
        service_class.return_value.bootstrap.return_value = self.result

        with (
            patch(
                "apps.datavionos.api.views.bootstrap.platform_bootstrap_builder"
            ) as builder,
            patch(
                "apps.datavionos.api.views.bootstrap.PlatformBootstrapSerializer"
            ) as serializer_class,
        ):
            builder.build.return_value = self.bootstrap
            serializer_class.return_value.data = {
                "organization": {"id": "workspace-organization"},
            }
            request = self.factory.get("/api/bootstrap/")
            force_authenticate(request, user=self.user)
            response = PlatformBootstrapAPIView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        service_class.return_value.bootstrap.assert_called_once_with(
            tenant="workspace-tenant",
            user=self.user,
            organization="workspace-organization",
            permissions={"workspace.view"},
        )

    @patch("apps.datavionos.api.views.bootstrap.PlatformBootstrapService")
    @patch("apps.datavionos.api.views.bootstrap.platform_bootstrap_selector")
    def test_bootstrap_result_feeds_dashboard_and_navigation_payload(
        self, selector, service_class
    ):
        selector.get.return_value = self.context
        service_class.return_value.bootstrap.return_value = self.result

        with (
            patch(
                "apps.datavionos.api.views.bootstrap.platform_bootstrap_builder"
            ) as builder,
            patch(
                "apps.datavionos.api.views.bootstrap.PlatformBootstrapSerializer"
            ) as serializer_class,
        ):
            builder.build.return_value = self.bootstrap
            serializer_class.return_value.data = {
                "modules": [{"identifier": "module-a"}],
                "navigation": [{"route": "/module-a"}],
                "dashboard": [{"route": "/module-a"}],
            }
            request = self.factory.get("/api/bootstrap/")
            force_authenticate(request, user=self.user)
            response = PlatformBootstrapAPIView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        kwargs = builder.build.call_args.kwargs
        self.assertEqual(kwargs["modules"], ("module-a",))
        self.assertEqual(kwargs["navigation"], ("navigation-a",))
        self.assertEqual(kwargs["dashboard"], ("dashboard-a",))
        self.assertEqual(kwargs["context"], self.context)

    def test_view_remains_thin_and_canonical(self):
        module = __import__(
            "apps.datavionos.api.views.bootstrap",
            fromlist=["__file__"],
        )
        source = Path(module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "EntitlementService(",
            "OrganizationModule.objects",
            "Subscription.objects",
            "has_permission(",
            "module_enabled(",
            "feature_enabled(",
        )
        for token in forbidden:
            self.assertNotIn(token, source)


__all__ = ["OrganizationWorkspaceBootstrapAPIRuntimeTests"]
