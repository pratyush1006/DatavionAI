from apps.common.permissions.base import BasePermission


class TelemedicinePermission:
    VIEW = "telemedicine.view"
    CREATE = "telemedicine.create"
    UPDATE = "telemedicine.update"
    CANCEL = "telemedicine.cancel"
    PREPARE = "telemedicine.prepare"
    START = "telemedicine.start"
    COMPLETE = "telemedicine.complete"
    PARTICIPANT = "telemedicine.participant.manage"
    RECORDING = "telemedicine.recording.manage"


class CanViewTelemedicineSession(BasePermission):
    permission_code = TelemedicinePermission.VIEW


class CanCreateTelemedicineSession(BasePermission):
    permission_code = TelemedicinePermission.CREATE


class CanCancelTelemedicineSession(BasePermission):
    permission_code = TelemedicinePermission.CANCEL


class CanPrepareTelemedicineSession(BasePermission):
    permission_code = TelemedicinePermission.PREPARE


class CanStartTelemedicineSession(BasePermission):
    permission_code = TelemedicinePermission.START


class CanCompleteTelemedicineSession(BasePermission):
    permission_code = TelemedicinePermission.COMPLETE


class CanManageTelemedicineParticipant(BasePermission):
    permission_code = TelemedicinePermission.PARTICIPANT


class CanManageTelemedicineRecording(BasePermission):
    permission_code = TelemedicinePermission.RECORDING
