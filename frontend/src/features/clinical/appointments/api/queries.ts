import {
  queryOptions,
} from "@tanstack/react-query";

import {
  apiClient,
} from "@/core/api";

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

type AppointmentListResponse = {
  data: AppointmentDto[];
};

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
  const {
    data,
  } =
    await apiClient.get<
      AppointmentListResponse
    >(
      appointmentEndpoints.collection,
    );

  return data.data.map(
    mapAppointment,
  );
}

export const appointmentQueries = {
  all: () =>
    queryOptions({
      queryKey:
        appointmentKeys.lists(),

      queryFn:
        fetchAppointments,
    }),
} as const;
