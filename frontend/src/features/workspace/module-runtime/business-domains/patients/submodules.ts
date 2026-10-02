export type PatientManagementSubmodule = {
  id: string;
  label: string;
  parentModule: "patients";
  protected: boolean;
};

/** Product composition only; authorization remains backend-owned. */
export const PATIENT_MANAGEMENT_SUBMODULES: readonly PatientManagementSubmodule[] = [
  { id: "registration", label: "Registration", parentModule: "patients", protected: false },
  { id: "patients", label: "Patients", parentModule: "patients", protected: false },
  { id: "profile", label: "Profile", parentModule: "patients", protected: false },
  { id: "mpi", label: "Master Patient Index", parentModule: "patients", protected: false },
  { id: "addresses", label: "Addresses", parentModule: "patients", protected: false },
  { id: "contacts", label: "Contacts", parentModule: "patients", protected: false },
  { id: "emergency", label: "Emergency", parentModule: "patients", protected: false },
  { id: "emergency_contacts", label: "Emergency Contacts", parentModule: "patients", protected: false },
  { id: "communication", label: "Communication", parentModule: "patients", protected: false },
  { id: "consents", label: "Consents", parentModule: "patients", protected: false },
  { id: "medical_history", label: "Medical History", parentModule: "patients", protected: false },
  { id: "relationships", label: "Relationships", parentModule: "patients", protected: false },
  { id: "family_members", label: "Family Members", parentModule: "patients", protected: true },
  { id: "referrals", label: "Referrals", parentModule: "patients", protected: false },
  { id: "patient_documents", label: "Patient Documents", parentModule: "patients", protected: false },
  { id: "portal", label: "Patient Portal", parentModule: "patients", protected: false },
  { id: "preferences", label: "Preferences", parentModule: "patients", protected: false },
  { id: "timeline", label: "Timeline", parentModule: "patients", protected: false },
];
