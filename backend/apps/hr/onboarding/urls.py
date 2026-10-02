from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.hr.onboarding.api.urls"),
    ),
]
