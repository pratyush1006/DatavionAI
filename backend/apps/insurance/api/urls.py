from django.urls import path

from apps.insurance.api.views import (
    MODELS,
    CollectionAPIView,
    DetailAPIView,
    RouteAPIView,
)

urlpatterns = []
for segment, model in MODELS.items():
    urlpatterns.append(
        path(
            f"{segment}/",
            type(
                f"{model.__name__}CollectionAPIView",
                (CollectionAPIView,),
                {"model": model},
            ).as_view(),
        )
    )
    urlpatterns.append(
        path(
            f"{segment}/<uuid:object_id>/",
            type(
                f"{model.__name__}DetailAPIView", (DetailAPIView,), {"model": model}
            ).as_view(),
        )
    )
urlpatterns.append(
    path(
        "enrollments/<uuid:enrollment_id>/resolve-route/<str:service>/",
        RouteAPIView.as_view(),
    )
)
