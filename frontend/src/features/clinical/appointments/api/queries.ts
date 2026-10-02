import {
  queryOptions,
} from "@tanstack/react-query";

import {
  apiClient,
} from "@/core/api";
import {
  patientEndpoints,
} from "@/features/clinical/patients/api/endpoints";

import type {
  Appointment,
} from "../domain";

import {
  appointmentEndpoints,
} from "./endpoints";

import {
  appointmentKeys,
} from "./keys";

type AppointmentDto =
  Record<string, unknown>;

export type AppointmentOption = {
  id: string;
  label: string;
};

export type AppointmentTracking = {
  appointment_number: string;
  status: Appointment["status"];
  scheduled_start: string;
  scheduled_end: string;
  deposit_paid: boolean;
  can_reschedule: boolean;
};

export async function fetchAppointmentTracking(
  token: string,
): Promise<AppointmentTracking> {
  const { data } = await apiClient.get<AppointmentTracking>(
    appointmentEndpoints.tracking(token),
  );
  return data;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function recordsFrom(value: unknown): AppointmentDto[] {
  if (Array.isArray(value)) {
    return value.filter(isRecord);
  }

  if (isRecord(value)) {
    for (const key of ["results", "items", "data"]) {
      if (key in value) {
        const records = recordsFrom(value[key]);
        if (records.length > 0 || Array.isArray(value[key])) {
          return records;
        }
      }
    }
  }

  return [];
}

function mapAppointment(
  dto: AppointmentDto,
): Appointment {
  return {
    id:
      String(dto.id),

    organization:
      String(dto.organization ?? ""),

    patient:
      String(dto.patient ?? ""),

    provider:
      String(dto.provider ?? ""),

    appointmentNumber:
      String(dto.appointment_number ?? ""),

    appointmentType:
      dto.appointment_type as Appointment["appointmentType"],

    status:
      dto.status as Appointment["status"],

    priority:
      dto.priority as Appointment["priority"],

    scheduledStart:
      String(dto.scheduled_start ?? ""),

    scheduledEnd:
      String(dto.scheduled_end ?? ""),

    durationMinutes:
      Number(dto.duration_minutes ?? 0),

    rescheduleCount:
      Number(dto.reschedule_count ?? 0),

    canReschedule:
      Boolean(dto.can_reschedule),

    consultationFee:
      Number(dto.consultation_fee ?? 0),

    depositAmount:
      Number(dto.deposit_amount ?? 0),

    depositInvoiceId:
      String(dto.deposit_invoice_id ?? ""),

    finalInvoiceId:
      String(dto.final_invoice_id ?? ""),

    depositPaid:
      Boolean(dto.deposit_paid),

    trackingToken:
      String(dto.tracking_token ?? ""),

    reason:
      String(dto.reason ?? ""),

    notes:
      String(dto.notes ?? ""),

    isVirtual:
      Boolean(dto.is_virtual),

    meetingUrl:
      String(dto.meeting_url ?? ""),

    isActive:
      Boolean(dto.is_active),
  };
}

async function fetchAppointments(): Promise<
  Appointment[]
> {
  const { data } = await apiClient.get<unknown>(
    appointmentEndpoints.collection,
    {
      // A clinical list must settle promptly. A stalled local/proxy
      // connection must show an actionable error instead of loading forever.
      timeout: 15_000,
    },
  );

  return recordsFrom(data).map(mapAppointment);
}

async function fetchPatients(): Promise<AppointmentOption[]> {
  const { data } = await apiClient.get<unknown>(
    `${patientEndpoints.collection}?page_size=100&is_active=true`,
  );

  return recordsFrom(data).map((patient) => ({
    id: String(patient.id ?? ""),
    label: `${String(patient.display_name ?? "Patient")} · ${String(patient.mrn ?? "")}`,
  })).filter((patient) => patient.id.length > 0);
}

async function fetchProviders(): Promise<AppointmentOption[]> {
  const { data } = await apiClient.get<unknown>(
    "/providers/?page_size=100&is_accepting_patients=true",
  );

  return recordsFrom(data).map((provider) => ({
    id: String(provider.id ?? ""),
    label: `${String(provider.provider_number ?? "Provider")} · ${String(provider.provider_type ?? "")} · ₹${Number(provider.consultation_fee ?? 0).toFixed(2)}`,
  })).filter((provider) => provider.id.length > 0);
}

export const appointmentQueries = {
  all: () =>
    queryOptions({
      queryKey:
        appointmentKeys.lists(),

      queryFn:
        fetchAppointments,

      retry: 1,

      refetchInterval: 15_000,
    }),

  patients: () =>
    queryOptions({
      queryKey: [...appointmentKeys.all, "patients"],
      queryFn: fetchPatients,
    }),

  providers: () =>
    queryOptions({
      queryKey: [...appointmentKeys.all, "providers"],
      queryFn: fetchProviders,
    }),
} as const;
