from apps.platform.rbac.permissions.base import RBACPermissionBase


class NotePermission:
    VIEW = "notes.view"
    CREATE = "notes.create"
    EDIT = "notes.update"
    REVIEW = "notes.approve"
    SIGN = "notes.sign"
    AMEND = "notes.update"
    CANCEL = "notes.cancel"


class CanViewNotes(RBACPermissionBase):
    permission_code = NotePermission.VIEW


class CanCreateNotes(RBACPermissionBase):
    permission_code = NotePermission.CREATE


class CanEditNotes(RBACPermissionBase):
    permission_code = NotePermission.EDIT


class CanReviewNotes(RBACPermissionBase):
    permission_code = NotePermission.REVIEW


class CanSignNotes(RBACPermissionBase):
    permission_code = NotePermission.SIGN


class CanAmendNotes(RBACPermissionBase):
    permission_code = NotePermission.AMEND


class CanCancelNotes(RBACPermissionBase):
    permission_code = NotePermission.CANCEL
