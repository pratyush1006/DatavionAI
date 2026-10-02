from django.urls import include, path

urlpatterns = [
    path("", include("apps.pharmacy.api.pharmacy_urls")),
]
