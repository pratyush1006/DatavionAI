/**
 * Organization domain options.
 */

/** Backend-authoritative Organization model choice values. */

type Option = Readonly<{ value: string; label: string }>;

const toOptions = (values: readonly (readonly [string, string])[]): readonly Option[] =>
  values.map(([value, label]) => ({ value, label }));

export const organizationCategoryOptions = toOptions([
  ["healthcare_provider", "Healthcare Provider"], ["diagnostics", "Diagnostics"], ["pharmacy", "Pharmacy"], ["emergency", "Emergency Services"],
  ["insurance", "Insurance"], ["research", "Research & Education"], ["public_health", "Public Health"], ["enterprise", "Enterprise"],
]);

export const organizationTypeOptions = toOptions([
  ["hospital", "Hospital"], ["clinic", "Clinic"], ["dental_clinic", "Dental Clinic"], ["eye_clinic", "Eye Clinic"], ["ent_clinic", "ENT Clinic"],
  ["cardiology_clinic", "Cardiology Clinic"], ["neurology_clinic", "Neurology Clinic"], ["orthopedic_clinic", "Orthopedic Clinic"], ["pediatric_clinic", "Pediatric Clinic"],
  ["gynecology_clinic", "Gynecology Clinic"], ["dermatology_clinic", "Dermatology Clinic"], ["psychiatry_clinic", "Psychiatry Clinic"], ["oncology_center", "Oncology Center"],
  ["physiotherapy_center", "Physiotherapy Center"], ["rehabilitation_center", "Rehabilitation Center"], ["dialysis_center", "Dialysis Center"], ["fertility_center", "Fertility Center"],
  ["home_healthcare", "Home Healthcare"], ["telemedicine", "Telemedicine Provider"], ["nursing_home", "Nursing Home"], ["hospice", "Hospice"], ["assisted_living", "Assisted Living Facility"],
  ["wellness_center", "Wellness Center"], ["laboratory", "Laboratory"], ["diagnostic_center", "Diagnostic Center"], ["radiology_center", "Radiology Center"],
  ["imaging_center", "Imaging Center"], ["pathology_lab", "Pathology Laboratory"], ["blood_bank", "Blood Bank"], ["retail_pharmacy", "Retail Pharmacy"],
  ["hospital_pharmacy", "Hospital Pharmacy"], ["online_pharmacy", "Online Pharmacy"], ["wholesale_pharmacy", "Wholesale Pharmacy"], ["ambulance_service", "Ambulance Service"],
  ["trauma_center", "Trauma Center"], ["emergency_center", "Emergency Center"], ["insurance_company", "Insurance Company"], ["tpa", "Third Party Administrator"],
  ["medical_college", "Medical College"], ["medical_university", "Medical University"], ["research_institute", "Research Institute"], ["clinical_trial_center", "Clinical Trial Center"],
  ["government_hospital", "Government Hospital"], ["public_health_center", "Public Health Center"], ["ngo", "NGO"], ["corporate", "Corporate"],
  ["occupational_health", "Occupational Health"], ["healthcare_network", "Healthcare Network"],
]);

export const organizationSizeOptions = toOptions([
  ["solo", "Solo Practice"], ["small", "Small"], ["medium", "Medium"], ["large", "Large"], ["enterprise", "Enterprise"],
]);

export const organizationStatusOptions = toOptions([
  ["draft", "Draft"], ["pending_verification", "Pending Verification"], ["active", "Active"], ["inactive", "Inactive"], ["suspended", "Suspended"], ["archived", "Archived"],
]);
