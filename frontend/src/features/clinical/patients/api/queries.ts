/**
 * =============================================================================
 * DatavionOS
 * File: src/features/clinical/patients/api/queries.ts
 * =============================================================================
 *
 * Patient query definitions.
 * =============================================================================
 */

import {
  queryOptions,
} from "@tanstack/react-query";

import {
  apiClient,
} from "@/core/api";

import type {
  Patient,
} from "../domain";

import {
  patientEndpoints,
} from "./endpoints";

import {
  patientKeys,
} from "./keys";

type PatientDto =
  Record<string, unknown>;

type PatientListResponse = {
  data: PatientDto[];
};

function mapPatient(
  dto: PatientDto,
): Patient {
  return {
    id: String(dto.id),

    organization:
      String(dto.organization ?? ""),

    mrn:
      String(dto.mrn ?? ""),

    firstName:
      String(dto.first_name ?? ""),

    middleName:
      String(dto.middle_name ?? ""),

    lastName:
      String(dto.last_name ?? ""),

    preferredName:
      String(dto.preferred_name ?? ""),

    displayName:
      String(dto.display_name ?? ""),

    age:
      Number(dto.age ?? 0),

    dateOfBirth:
      String(dto.date_of_birth ?? ""),

    gender:
      String(
        dto.gender ?? "UNKNOWN",
      ).toUpperCase() as Patient["gender"],

    maritalStatus:
      String(dto.marital_status ?? ""),

    bloodGroup:
      String(dto.blood_group ?? ""),

    phone:
      String(dto.phone ?? ""),

    email:
      String(dto.email ?? ""),

    address:
      String(dto.address ?? ""),

    city:
      String(dto.city ?? ""),

    state:
      String(dto.state ?? ""),

    country:
      String(dto.country ?? "India"),

    postalCode:
      String(dto.postal_code ?? ""),

    status:
      String(
        dto.status ?? "ACTIVE",
      ).toUpperCase() as Patient["status"],

    isActive:
      Boolean(dto.is_active),
  };
}

async function fetchPatients(): Promise<
  Patient[]
> {
  const {
    data,
  } =
    await apiClient.get<
      PatientListResponse
    >(
      patientEndpoints.collection,
    );

  return data.data.map(
    mapPatient,
  );
}

export const patientQueries = {
  all: () =>
    queryOptions({
      queryKey:
        patientKeys.lists(),

      queryFn:
        fetchPatients,
    }),
} as const;
