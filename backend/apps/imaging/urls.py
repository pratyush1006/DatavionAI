from django.urls import include, path

urlpatterns = [
    path("", include("apps.imaging.api.urls")),
]
