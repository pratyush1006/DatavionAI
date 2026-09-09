from django.urls import include, path

urlpatterns = [path("", include("apps.device_platform.api.urls"))]
