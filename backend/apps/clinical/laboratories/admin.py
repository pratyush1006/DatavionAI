from django.contrib import admin

from .models import (
    Laboratory,
    LaboratoryAuditLog,
    LaboratoryDepartment,
    LaboratoryOrder,
    LaboratoryOrderItem,
    LaboratoryOutboxEvent,
    LaboratoryPanelItem,
    LaboratoryReport,
    LaboratoryResult,
    LaboratorySlot,
    LaboratorySpecimen,
    LaboratoryTest,
)

admin.site.register(
    [
        Laboratory,
        LaboratoryDepartment,
        LaboratoryTest,
        LaboratoryPanelItem,
        LaboratorySlot,
        LaboratoryOrder,
        LaboratoryOrderItem,
        LaboratorySpecimen,
        LaboratoryResult,
        LaboratoryReport,
        LaboratoryAuditLog,
        LaboratoryOutboxEvent,
    ]
)
