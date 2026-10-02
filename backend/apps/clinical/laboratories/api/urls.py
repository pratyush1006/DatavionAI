from django.urls import path

from .health import LaboratoryHealthAPIView
from .laboratory_urls import urlpatterns as laboratory_urlpatterns

urlpatterns = [
    path("health/", LaboratoryHealthAPIView.as_view(), name="laboratories-health")
] + laboratory_urlpatterns
