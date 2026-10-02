from apps.platform.rbac.permissions.base import RBACPermissionBase


class CanViewPharmacy(RBACPermissionBase):
    permission_code = "pharmacy.view"
    message = "You do not have permission to view pharmacy data."


class CanManageInventory(RBACPermissionBase):
    permission_code = "pharmacy.inventory"
    message = "You do not have permission to manage pharmacy inventory."


class CanManagePurchasing(RBACPermissionBase):
    permission_code = "pharmacy.purchasing"
    message = "You do not have permission to manage pharmacy purchasing."


class CanManageControlledSubstances(RBACPermissionBase):
    permission_code = "pharmacy.controlled"
    message = "You do not have permission to manage controlled-substance operations."


class CanManageRecalls(RBACPermissionBase):
    permission_code = "pharmacy.recall"
    message = "You do not have permission to manage pharmacy recalls."


class CanApprovePurchasing(RBACPermissionBase):
    permission_code = "pharmacy.purchasing.approve"
    message = "You do not have permission to approve pharmacy purchasing."


class CanDispenseMedication(RBACPermissionBase):
    permission_code = "pharmacy.dispense"
    message = "You do not have permission to dispense medication."


class CanManagePharmacy(RBACPermissionBase):
    permission_code = "pharmacy.manage"
    message = "You do not have permission to manage pharmacy master data."
