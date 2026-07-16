from apps.clinical.laboratories.api.views.laboratory_order import (
    LaboratoryOrderListCreateAPIView,
    LaboratoryOrderRetrieveUpdateDestroyAPIView,
)

###############################################################################
# Laboratory Result
###############################################################################
from apps.clinical.laboratories.api.views.laboratory_result import (
    LaboratoryResultAmendAPIView,
    LaboratoryResultInvalidateAPIView,
    LaboratoryResultListCreateAPIView,
    LaboratoryResultRecordAPIView,
    LaboratoryResultRetrieveUpdateDestroyAPIView,
    LaboratoryResultVerifyAPIView,
)
from apps.clinical.laboratories.api.views.laboratory_test import (
    LaboratoryTestListCreateAPIView,
    LaboratoryTestRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "LaboratoryOrderListCreateAPIView",
    "LaboratoryOrderRetrieveUpdateDestroyAPIView",
    "LaboratoryTestListCreateAPIView",
    "LaboratoryTestRetrieveUpdateDestroyAPIView",
    "LaboratoryResultListCreateAPIView",
    "LaboratoryResultRetrieveUpdateDestroyAPIView",
    "LaboratoryResultRecordAPIView",
    "LaboratoryResultVerifyAPIView",
    "LaboratoryResultAmendAPIView",
    "LaboratoryResultInvalidateAPIView",
]
