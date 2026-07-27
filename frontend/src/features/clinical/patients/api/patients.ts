import { apiClient } from "@/core/api";

import type { Patient, PatientFormValues } from "../domain/types";

type PatientDto = Record<string, unknown>;
type ListResponse = { data: PatientDto[] };

function mapPatient(dto: PatientDto): Patient {
  return {
    id: String(dto.id), organization: String(dto.organization ?? ""), mrn: String(dto.mrn),
    firstName: String(dto.first_name ?? ""), middleName: String(dto.middle_name ?? ""),
    lastName: String(dto.last_name ?? ""), preferredName: String(dto.preferred_name ?? ""),
    displayName: String(dto.display_name ?? ""), age: Number(dto.age ?? 0),
    dateOfBirth: String(dto.date_of_birth ?? ""), gender: String(dto.gender ?? "UNKNOWN").toUpperCase() as Patient["gender"],
    maritalStatus: String(dto.marital_status ?? ""), bloodGroup: String(dto.blood_group ?? ""),
    phone: String(dto.phone ?? ""), email: String(dto.email ?? ""), address: String(dto.address ?? ""),
    city: String(dto.city ?? ""), state: String(dto.state ?? ""), country: String(dto.country ?? "India"),
    postalCode: String(dto.postal_code ?? ""), status: String(dto.status ?? "ACTIVE").toUpperCase() as Patient["status"],
    isActive: Boolean(dto.is_active),
  };
}

function toPayload(values: PatientFormValues) {
  return {
    organization: values.organization, mrn: values.mrn, first_name: values.firstName,
    middle_name: values.middleName, last_name: values.lastName, preferred_name: values.preferredName,
    date_of_birth: values.dateOfBirth, gender: values.gender.toLowerCase(),
    marital_status: values.maritalStatus.toLowerCase(), blood_group: values.bloodGroup,
    phone: values.phone, email: values.email, address: values.address, city: values.city,
    state: values.state, country: values.country, postal_code: values.postalCode,
    status: values.status.toLowerCase(), is_active: values.isActive,
  };
}

export async function fetchPatients() {
  const { data } = await apiClient.get<ListResponse>("/patients/");
  return data.data.map(mapPatient);
}

export async function createPatient(values: PatientFormValues) {
  const { data } = await apiClient.post<PatientDto>("/patients/", toPayload(values));
  return mapPatient(data);
}

export async function updatePatient({ id, values }: { id: string; values: PatientFormValues }) {
  const { organization: _organization, mrn: _mrn, ...payload } = toPayload(values);
  const { data } = await apiClient.patch<PatientDto>(`/patients/${id}/`, payload);
  return mapPatient(data);
}

export async function deletePatient(id: string) { await apiClient.delete(`/patients/${id}/`); }
