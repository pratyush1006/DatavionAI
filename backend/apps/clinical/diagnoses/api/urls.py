from django.urls import path

from .views import DiagnosisDetailAPIView, DiagnosisListCreateAPIView

urlpatterns = [
    path("", DiagnosisListCreateAPIView.as_view(), name="list-create"),
    path("<uuid:diagnosis_id>/", DiagnosisDetailAPIView.as_view(), name="detail"),
]
