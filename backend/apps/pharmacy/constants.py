from django.db import models


class PharmacyStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class PurchaseOrderStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ORDERED = "ordered", "Ordered"
    PARTIALLY_RECEIVED = "partially_received", "Partially Received"
    RECEIVED = "received", "Received"
    CANCELLED = "cancelled", "Cancelled"


class StockMovementType(models.TextChoices):
    RECEIPT = "receipt", "Receipt"
    DISPENSE = "dispense", "Dispense"
    PATIENT_RETURN = "patient_return", "Patient Return"
    SUPPLIER_RETURN = "supplier_return", "Supplier Return"
    ADJUSTMENT = "adjustment", "Adjustment"
    TRANSFER_IN = "transfer_in", "Transfer In"
    TRANSFER_OUT = "transfer_out", "Transfer Out"


class DispenseStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    READY = "ready", "Ready"
    DISPENSED = "dispensed", "Dispensed"
    PARTIAL = "partial", "Partially Dispensed"
    CANCELLED = "cancelled", "Cancelled"


class ReturnType(models.TextChoices):
    PATIENT = "patient", "Patient"
    SUPPLIER = "supplier", "Supplier"


class ControlledSubstanceSchedule(models.TextChoices):
    NONE = "none", "Not Controlled"
    SCHEDULE_I = "schedule_i", "Schedule I"
    SCHEDULE_II = "schedule_ii", "Schedule II"
    SCHEDULE_III = "schedule_iii", "Schedule III"
    SCHEDULE_IV = "schedule_iv", "Schedule IV"
    SCHEDULE_V = "schedule_v", "Schedule V"


class QuarantineStatus(models.TextChoices):
    QUARANTINED = "quarantined", "Quarantined"
    RELEASED = "released", "Released"
    DESTROYED = "destroyed", "Destroyed"


class RecallStatus(models.TextChoices):
    OPEN = "open", "Open"
    IN_PROGRESS = "in_progress", "In Progress"
    CLOSED = "closed", "Closed"


class ApprovalStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class BillingStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    INVOICED = "invoiced", "Invoiced"
    PAID = "paid", "Paid"
    VOID = "void", "Void"


class ReservationStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    RELEASED = "released", "Released"
    COMMITTED = "committed", "Committed"
    EXPIRED = "expired", "Expired"
    CANCELLED = "cancelled", "Cancelled"


class TransferOrderStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    APPROVED = "approved", "Approved"
    IN_TRANSIT = "in_transit", "In Transit"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
