"""
Serializers for the Laboratories application.
"""

###############################################################################
# Laboratory Order
###############################################################################

from apps.clinical.laboratories.api.serializers.laboratory_order import (
    LaboratoryOrderCreateSerializer,
    LaboratoryOrderDetailSerializer,
    LaboratoryOrderListSerializer,
    LaboratoryOrderSerializer,
    LaboratoryOrderUpdateSerializer,
)

###############################################################################
# Laboratory Result
###############################################################################
from apps.clinical.laboratories.api.serializers.laboratory_result import (
    LaboratoryResultCreateSerializer,
    LaboratoryResultDetailSerializer,
    LaboratoryResultListSerializer,
    LaboratoryResultSerializer,
    LaboratoryResultUpdateSerializer,
)

###############################################################################
# Laboratory Test
###############################################################################
from apps.clinical.laboratories.api.serializers.laboratory_test import (
    LaboratoryTestCreateSerializer,
    LaboratoryTestDetailSerializer,
    LaboratoryTestListSerializer,
    LaboratoryTestSerializer,
    LaboratoryTestUpdateSerializer,
)

__all__ = [
    ############################################################################
    # Laboratory Order
    ############################################################################
    "LaboratoryOrderSerializer",
    "LaboratoryOrderCreateSerializer",
    "LaboratoryOrderUpdateSerializer",
    "LaboratoryOrderListSerializer",
    "LaboratoryOrderDetailSerializer",
    ############################################################################
    # Laboratory Test
    ############################################################################
    "LaboratoryTestSerializer",
    "LaboratoryTestCreateSerializer",
    "LaboratoryTestUpdateSerializer",
    "LaboratoryTestListSerializer",
    "LaboratoryTestDetailSerializer",
    ############################################################################
    # Laboratory Result
    ############################################################################
    "LaboratoryResultSerializer",
    "LaboratoryResultCreateSerializer",
    "LaboratoryResultUpdateSerializer",
    "LaboratoryResultListSerializer",
    "LaboratoryResultDetailSerializer",
]
