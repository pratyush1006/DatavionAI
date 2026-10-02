from apps.clinical.diagnoses.workflows import (
    DiagnosisCreateWorkflow,
    DiagnosisDeleteWorkflow,
    DiagnosisUpdateWorkflow,
)

WORKFLOW_REGISTRY = {
    "diagnosis.create": DiagnosisCreateWorkflow,
    "diagnosis.update": DiagnosisUpdateWorkflow,
    "diagnosis.delete": DiagnosisDeleteWorkflow,
}
