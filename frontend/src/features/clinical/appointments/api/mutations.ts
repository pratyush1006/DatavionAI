import {
  mutationOptions,
} from "@tanstack/react-query";

import {
  apiClient,
} from "@/core/api";

import type {
  Appointment,
  AppointmentFormValues,
} from "../domain";

import {
  appointmentEndpoints,
} from "./endpoints";

type AppointmentDto =
  Record<string, unknown>;

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

function toPayload(
  values: AppointmentFormValues,
) {
  return {
    organization:
      values.organization,

    patient:
      values.patient,

    provider:
      values.provider,

    appointment_number:
      values.appointmentNumber,

    appointment_type:
      values.appointmentType,

    status:
      values.status,

    priority:
      values.priority,

    scheduled_start:
      values.scheduledStart,

    scheduled_end:
      values.scheduledEnd,

    duration_minutes:
      values.durationMinutes,

    reason:
      values.reason,

    notes:
      values.notes,

    is_virtual:
      values.isVirtual,

    meeting_url:
      values.meetingUrl,

    is_active:
      values.isActive,
  };
}

async function createAppointment(
  values: AppointmentFormValues,
): Promise<Appointment> {
  const {
    data,
  } =
    await apiClient.post<AppointmentDto>(
      appointmentEndpoints.collection,
      toPayload(values),
    );

  return mapAppointment(data);
}

async function updateAppointment({
  id,
  values,
}: {
  id: string;
  values: AppointmentFormValues;
}): Promise<Appointment> {
  const {
    data,
  } =
    await apiClient.patch<AppointmentDto>(
      appointmentEndpoints.byId(id),
      toPayload(values),
    );

  return mapAppointment(data);
}

async function deleteAppointment(
  id: string,
): Promise<void> {
  await apiClient.delete(
    appointmentEndpoints.byId(id),
  );
}

export const appointmentMutations = {
  create: () =>
    mutationOptions({
      mutationFn:
        createAppointment,
    }),

  update: () =>
    mutationOptions({
      mutationFn:
        updateAppointment,
    }),

  delete: () =>
    mutationOptions({
      mutationFn:
        deleteAppointment,
    }),
} as const;
