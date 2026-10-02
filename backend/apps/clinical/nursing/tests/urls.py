from django.urls import include, path

urlpatterns = [path("api/nursing/", include("apps.clinical.nursing.urls"))]
