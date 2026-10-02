from django.urls import include, path

app_name = "patient-relationships"
urlpatterns = (
    path("", include("apps.patient_management.relationships.api.urls.relationship")),
)
