from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.teams.api.urls"),
    ),
]
