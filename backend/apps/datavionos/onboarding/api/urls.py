from django.urls import path

from apps.datavionos.onboarding.api.catalog import (
    OrganizationCatalogAPIView,
)
from apps.datavionos.onboarding.api.signup_views import (
    SelfServiceSignupAPIView,
    SelfServiceSignupPreflightAPIView,
)
from apps.datavionos.onboarding.api.views import (
    OrganizationOnboardingStatusAPIView,
    OrganizationRegistrationPreflightAPIView,
    OrganizationTypeListAPIView,
    RegisterOrganizationAPIView,
    SaaSPlanListAPIView,
)

app_name = "organization-onboarding"

urlpatterns = [
    path(
        "signup/preflight/",
        SelfServiceSignupPreflightAPIView.as_view(),
        name="signup-preflight",
    ),
    path("signup/", SelfServiceSignupAPIView.as_view(), name="signup"),
    path(
        "catalog/",
        OrganizationCatalogAPIView.as_view(),
        name="catalog",
    ),
    path(
        "organization-types/",
        OrganizationTypeListAPIView.as_view(),
        name="organization-types",
    ),
    path(
        "plans/",
        SaaSPlanListAPIView.as_view(),
        name="plans",
    ),
    path(
        "register/preflight/",
        OrganizationRegistrationPreflightAPIView.as_view(),
        name="register-preflight",
    ),
    path(
        "register/",
        RegisterOrganizationAPIView.as_view(),
        name="register",
    ),
    path(
        "status/",
        OrganizationOnboardingStatusAPIView.as_view(),
        name="status",
    ),
]
