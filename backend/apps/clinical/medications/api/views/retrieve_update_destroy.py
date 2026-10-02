from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from apps.clinical.medications.api.serializers import (
    MedicationDetailSerializer,
    MedicationUpdateSerializer,
)
from apps.clinical.medications.permissions import MedicationPermission
from apps.clinical.medications.selectors import get_medication
from apps.clinical.medications.workflows.medication import MedicationWorkflow


class MedicationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (MedicationPermission,)
    lookup_url_kwarg = "medication_id"

    def get_organization(self):
        organization = getattr(self.request, "organization", None)
        if organization is None:
            organization = getattr(self.request.user, "organization", None)
        if organization is None:
            raise ValidationError("Organization context is required.")
        return organization

    def get_object(self):
        return get_medication(
            organization=self.get_organization(),
            medication_id=self.kwargs[self.lookup_url_kwarg],
        )

    def get_serializer_class(self):
        if self.request.method in {"PUT", "PATCH"}:
            return MedicationUpdateSerializer
        return MedicationDetailSerializer

    def perform_update(self, serializer):
        serializer.instance = MedicationWorkflow.update(
            organization=self.get_organization(),
            instance=self.get_object(),
            validated_data=serializer.validated_data,
            actor=self.request.user,
        )

    def perform_destroy(self, instance):
        MedicationWorkflow.delete(
            organization=self.get_organization(),
            instance=instance,
            actor=self.request.user,
        )
