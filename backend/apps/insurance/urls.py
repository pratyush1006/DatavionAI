from django.urls import include, path

urlpatterns = [path("", include("apps.insurance.api.urls"))]
