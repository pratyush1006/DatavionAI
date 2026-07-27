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

export type PatientFormValues = Omit<Patient, "id" | "displayName" | "age">;
