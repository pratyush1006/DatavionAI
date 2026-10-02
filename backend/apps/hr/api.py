"""Service-driven HR views using the platform response and serializer contracts."""

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)


class HrListCreateAPIView(BaseListCreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = type(self).create_service(validated_data=serializer.validated_data)
        output = self.detail_serializer_class(
            instance, context=self.get_serializer_context()
        )
        return self.created_response(
            data=output.data, message=self.create_success_message
        )


class HrRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=kwargs.pop("partial", False)
        )
        serializer.is_valid(raise_exception=True)
        instance = type(self).update_service(
            instance=instance, validated_data=serializer.validated_data
        )
        output = self.detail_serializer_class(
            instance, context=self.get_serializer_context()
        )
        return self.success_response(
            data=output.data, message=self.update_success_message
        )

    def destroy(self, request, *args, **kwargs):
        type(self).delete_service(instance=self.get_object())
        return self.no_content_response()
