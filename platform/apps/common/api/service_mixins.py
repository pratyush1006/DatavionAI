"""
Reusable API service mixins.

These mixins provide reusable CRUD orchestration while
delegating business logic to the service layer.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from .responses import (
    created_response,
    no_content_response,
    success_response,
)


class CreateServiceMixin:
    """
    Reusable POST implementation.

    Required attributes:
        create_service
        detail_serializer_class
        create_success_message
    """

    create_service: Callable[..., object]
    detail_serializer_class: type[BaseSerializer]
    create_success_message = "Created successfully."

    def create(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Validate request data, execute the create service,
        and return the serialized resource.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        instance = self.create_service(
            validated_data=serializer.validated_data,
        )

        detail_serializer = self.detail_serializer_class(
            instance,
            context=self.get_serializer_context(),
        )

        return created_response(
            data=detail_serializer.data,
            message=self.create_success_message,
        )


class UpdateServiceMixin:
    """
    Reusable PUT/PATCH implementation.

    Required attributes:
        update_service
        detail_serializer_class
        update_success_message
    """

    update_service: Callable[..., object]
    detail_serializer_class: type[BaseSerializer]
    update_success_message = "Updated successfully."

    def _update(
        self,
        request: Request,
        *,
        partial: bool,
    ) -> Response:
        """
        Execute a full or partial update.
        """

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        instance = self.update_service(
            instance=instance,
            validated_data=serializer.validated_data,
        )

        detail_serializer = self.detail_serializer_class(
            instance,
            context=self.get_serializer_context(),
        )

        return success_response(
            data=detail_serializer.data,
            message=self.update_success_message,
        )

    def update(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Handle HTTP PUT requests.
        """

        return self._update(
            request,
            partial=False,
        )

    def partial_update(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Handle HTTP PATCH requests.
        """

        return self._update(
            request,
            partial=True,
        )


class DestroyServiceMixin:
    """
    Reusable DELETE implementation.

    Required attributes:
        delete_service
    """

    delete_service: Callable[..., None]

    def destroy(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Delete the requested resource.
        """

        instance = self.get_object()

        self.delete_service(
            instance=instance,
        )

        return no_content_response()
