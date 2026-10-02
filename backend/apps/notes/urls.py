from django.urls import include, path

urlpatterns = [path("", include("apps.notes.api.urls"))]
