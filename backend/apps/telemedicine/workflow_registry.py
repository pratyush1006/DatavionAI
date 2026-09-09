from apps.core.workflows import workflow_registry
from apps.telemedicine.workflows import *


def register_telemedicine_workflows():
    for name, cls in {
        "telemedicine.session.create": SessionCreationWorkflow,
        "telemedicine.session.schedule": SessionSchedulingWorkflow,
        "telemedicine.session.confirm": SessionConfirmationWorkflow,
        "telemedicine.session.prepare": SessionPreparationWorkflow,
        "telemedicine.session.start": SessionStartWorkflow,
        "telemedicine.session.complete": SessionCompletionWorkflow,
        "telemedicine.session.cancel": SessionCancellationWorkflow,
        "telemedicine.session.no_show": SessionNoShowWorkflow,
        "telemedicine.session.fail": SessionFailureWorkflow,
        "telemedicine.participant.invite": ParticipantInvitationWorkflow,
        "telemedicine.participant.admit": ParticipantAdmissionWorkflow,
        "telemedicine.participant.join": ParticipantJoinWorkflow,
        "telemedicine.participant.leave": ParticipantLeaveWorkflow,
        "telemedicine.participant.media_state": ParticipantMediaStateWorkflow,
        "telemedicine.recording.start": RecordingStartWorkflow,
        "telemedicine.recording.finalize": RecordingFinalizeWorkflow,
    }.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=cls)
