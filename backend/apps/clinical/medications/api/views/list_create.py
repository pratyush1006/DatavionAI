from apps.clinical.medications.api.serializers import (
    MedicationCreateSerializer,
    MedicationListSerializer,
)
from apps.clinical.medications.permissions import MedicationPermission
from apps.clinical.medications.selectors import medication_queryset
from apps.clinical.medications.workflows.medication import MedicationWorkflow


def _organization(request):
    organization = getattr(request, "organization", None)
    if organization is not None:
        return organization
    return getattr(request.user, "organization", None)


class MedicationListCreateAPIView:
    permission_classes = (MedicationPermission,)

    @classmethod
    def as_view(cls):
        from rest_framework.generics import ListCreateAPIView

        class BoundView(ListCreateAPIView):
            permission_classes = cls.permission_classes

            def get_organization(self):
                organization = _organization(self.request)
                if organization is None:
                    from rest_framework.exceptions import ValidationError

                    raise ValidationError("Organization context is required.")
                return organization

            def get_queryset(self):
                return medication_queryset(organization=self.get_organization())

            def get_serializer_class(self):
                return (
                    MedicationCreateSerializer
                    if self.request.method == "POST"
                    else MedicationListSerializer
                )

            def perform_create(self, serializer):
                medication = MedicationWorkflow.create(
                    organization=self.get_organization(),
                    validated_data=serializer.validated_data,
                    actor=self.request.user,
                )
                serializer.instance = medication

        return BoundView.as_view()
