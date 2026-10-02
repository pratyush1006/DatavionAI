export const PATIENT_GENDERS = ["MALE", "FEMALE", "OTHER", "UNKNOWN"] as const;
export const PATIENT_STATUSES = ["ACTIVE", "INACTIVE", "DECEASED"] as const;

export type PatientGender = (typeof PATIENT_GENDERS)[number];
export type PatientStatus = (typeof PATIENT_STATUSES)[number];

export type Patient = {
  id: string;
  organization: string;
  mrn: string;
  firstName: string;
  middleName: string;
  lastName: string;
  preferredName: string;
  displayName: string;
  age: number;
  dateOfBirth: string;
  gender: PatientGender;
  maritalStatus: string;
  bloodGroup: string;
  phone: string;
  email: string;
  address: string;
  city: string;
  state: string;
  country: string;
  postalCode: string;
  status: PatientStatus;
  isActive: boolean;
};

// Organization ownership and MRN allocation are backend-controlled.  Keeping
// them out of editable form state prevents an operator from changing either
// identifier and keeps the Zod form contract aligned with the API payload.
export type PatientFormValues = Omit<
  Patient,
  "id" | "organization" | "mrn" | "displayName" | "age"
>;
