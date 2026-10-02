"""Canonical Patient Management product-domain catalog."""

PATIENT_MANAGEMENT_MODULE = "patients"

PATIENT_MANAGEMENT_SUBMODULES = {
    "registration": {"label": "Registration", "parent": "patients", "protected": False},
    "patients": {"label": "Patients", "parent": "patients", "protected": False},
    "profile": {"label": "Profile", "parent": "patients", "protected": False},
    "mpi": {"label": "Master Patient Index", "parent": "patients", "protected": False},
    "addresses": {"label": "Addresses", "parent": "patients", "protected": False},
    "contacts": {"label": "Contacts", "parent": "patients", "protected": False},
    "emergency": {"label": "Emergency", "parent": "patients", "protected": False},
    "emergency_contacts": {
        "label": "Emergency Contacts",
        "parent": "patients",
        "protected": False,
    },
    "communication": {
        "label": "Communication",
        "parent": "patients",
        "protected": False,
    },
    "consents": {"label": "Consents", "parent": "patients", "protected": False},
    "medical_history": {
        "label": "Medical History",
        "parent": "patients",
        "protected": False,
    },
    "relationships": {
        "label": "Relationships",
        "parent": "patients",
        "protected": False,
    },
    "family_members": {
        "label": "Family Members",
        "parent": "patients",
        "protected": True,
    },
    "referrals": {"label": "Referrals", "parent": "patients", "protected": False},
    "patient_documents": {
        "label": "Patient Documents",
        "parent": "patients",
        "protected": False,
    },
    "portal": {"label": "Patient Portal", "parent": "patients", "protected": False},
    "preferences": {"label": "Preferences", "parent": "patients", "protected": False},
    "timeline": {"label": "Timeline", "parent": "patients", "protected": False},
}

PROTECTED_SUBMODULES = frozenset(
    key for key, value in PATIENT_MANAGEMENT_SUBMODULES.items() if value["protected"]
)
