/**
 * =============================================================================
 * DatavionOS
 * File: src/features/clinical/patients/api/mutations.ts
 * =============================================================================
 *
 * Patient mutation definitions.
 *
 * Responsibilities
 * ----------------
 * - Create patient records
 * - Update mutable patient fields
 * - Delete patient records
 * - Map backend DTOs to frontend domain models
 * - Keep patient API mutations isolated from UI components
 *
 * Design Principles
 * -----------------
 * - Feature-owned API boundary
 * - Typed domain contracts
 * - Immutable patient identifiers on update
 * - No UI dependencies
 * - Reusable TanStack Query mutation definitions
 * - Backend field-name normalization
 * - Enterprise Ready
 * =============================================================================
 */

import {
  mutationOptions,
} from "@tanstack/react-query";

import {
  apiClient,
} from "@/core/api";

import type {
  Patient,
  PatientFormValues,
} from "../domain";

import {
  patientEndpoints,
} from "./endpoints";

/* =============================================================================
 * Backend DTO
 * =============================================================================
 */

/**
 * Backend patient response DTO.
 *
 * The backend response is intentionally treated as an unknown-keyed object
 * because the API client already owns transport/envelope validation while
 * this feature owns domain mapping.
 */
type PatientDto =
  Record<string, unknown>;

/* =============================================================================
 * DTO → Domain Mapping
 * =============================================================================
 */

/**
 * Convert a backend patient DTO into the frontend Patient domain model.
 */
function mapPatient(
  dto: PatientDto,
): Patient {
  return {
    id:
      String(
        dto.id,
      ),

    organization:
      String(
        dto.organization ?? "",
      ),

    mrn:
      String(
        dto.mrn ?? "",
      ),

    firstName:
      String(
        dto.first_name ?? "",
      ),

    middleName:
      String(
        dto.middle_name ?? "",
      ),

    lastName:
      String(
        dto.last_name ?? "",
      ),

    preferredName:
      String(
        dto.preferred_name ?? "",
      ),

    displayName:
      String(
        dto.display_name ?? "",
      ),

    age:
      Number(
        dto.age ?? 0,
      ),

    dateOfBirth:
      String(
        dto.date_of_birth ?? "",
      ),

    gender:
      String(
        dto.gender ?? "UNKNOWN",
      ).toUpperCase() as Patient["gender"],

    maritalStatus:
      String(
        dto.marital_status ?? "",
      ),

    bloodGroup:
      String(
        dto.blood_group ?? "",
      ),

    phone:
      String(
        dto.phone ?? "",
      ),

    email:
      String(
        dto.email ?? "",
      ),

    address:
      String(
        dto.address ?? "",
      ),

    city:
      String(
        dto.city ?? "",
      ),

    state:
      String(
        dto.state ?? "",
      ),

    country:
      String(
        dto.country ?? "India",
      ),

    postalCode:
      String(
        dto.postal_code ?? "",
      ),

    status:
      String(
        dto.status ?? "ACTIVE",
      ).toUpperCase() as Patient["status"],

    isActive:
      Boolean(
        dto.is_active,
      ),
  };
}

/* =============================================================================
 * Form → Backend Payload
 * =============================================================================
 */

/**
 * Convert frontend patient form values into the backend API representation.
 *
 * Organization ownership and MRN allocation are backend-owned. The active
 * organization comes from the authenticated request context and the backend
 * creates the MRN atomically during patient registration.
 */
function toPayload(
  values: PatientFormValues,
) {
  return {
    first_name:
      values.firstName,

    middle_name:
      values.middleName,

    last_name:
      values.lastName,

    preferred_name:
      values.preferredName,

    date_of_birth:
      values.dateOfBirth,

    gender:
      values.gender.toLowerCase(),

    marital_status:
      values.maritalStatus.toLowerCase(),

    blood_group:
      values.bloodGroup,

    phone:
      values.phone,

    email:
      values.email,

    address:
      values.address,

    city:
      values.city,

    state:
      values.state,

    country:
      values.country,

    postal_code:
      values.postalCode,

    status:
      values.status.toLowerCase(),

    is_active:
      values.isActive,
  };
}

/**
 * Payload accepted by the patient PATCH endpoint.
 *
 * Organization and MRN are never client mutation fields.
 */
type PatientUpdatePayload =
  Omit<
    ReturnType<typeof toPayload>,
    "organization" | "mrn"
  >;

/* =============================================================================
 * Create
 * =============================================================================
 */

/**
 * Create a patient.
 */
async function createPatient(
  values: PatientFormValues,
): Promise<Patient> {
  const {
    data,
  } =
    await apiClient.post<PatientDto>(
      patientEndpoints.collection,
      toPayload(values),
    );

  return mapPatient(
    data,
  );
}

/* =============================================================================
 * Update
 * =============================================================================
 */

/**
 * Update mutable patient fields.
 *
 * Organization and MRN are intentionally not included in the PATCH payload.
 */
async function updatePatient({
  id,
  values,
}: {
  id: string;
  values: PatientFormValues;
}): Promise<Patient> {
  const source =
    toPayload(values);

  const payload: PatientUpdatePayload = {
    first_name:
      source.first_name,

    middle_name:
      source.middle_name,

    last_name:
      source.last_name,

    preferred_name:
      source.preferred_name,

    date_of_birth:
      source.date_of_birth,

    gender:
      source.gender,

    marital_status:
      source.marital_status,

    blood_group:
      source.blood_group,

    phone:
      source.phone,

    email:
      source.email,

    address:
      source.address,

    city:
      source.city,

    state:
      source.state,

    country:
      source.country,

    postal_code:
      source.postal_code,

    status:
      source.status,

    is_active:
      source.is_active,
  };

  const {
    data,
  } =
    await apiClient.patch<PatientDto>(
      patientEndpoints.byId(
        id,
      ),
      payload,
    );

  return mapPatient(
    data,
  );
}

/* =============================================================================
 * Delete
 * =============================================================================
 */

/**
 * Delete a patient.
 */
async function deletePatient(
  id: string,
): Promise<void> {
  await apiClient.delete(
    patientEndpoints.byId(
      id,
    ),
  );
}

/* =============================================================================
 * Public Mutation Definitions
 * =============================================================================
 */

/**
 * TanStack Query mutation definitions for the patient feature.
 *
 * Hooks consume these definitions through the feature's mutation hook layer.
 */
export const patientMutations = {
  create: () =>
    mutationOptions({
      mutationFn:
        createPatient,
    }),

  update: () =>
    mutationOptions({
      mutationFn:
        updatePatient,
    }),

  delete: () =>
    mutationOptions({
      mutationFn:
        deletePatient,
    }),
} as const;
