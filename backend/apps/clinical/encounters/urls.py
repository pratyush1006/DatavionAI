from django.urls import include, path

app_name = "encounters"

urlpatterns = [path("", include("apps.clinical.encounters.api.urls"))]
