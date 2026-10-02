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

function toCreatePayload(values: AppointmentFormValues) {
  return {
    patient_id: values.patient,
    provider_id: values.provider,

    appointment_number:
      values.appointmentNumber,

    appointment_type:
      values.appointmentType,

    priority:
      values.priority,

    scheduled_start:
      new Date(values.scheduledStart).toISOString(),

    scheduled_end:
      new Date(values.scheduledEnd).toISOString(),

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

  };
}

function toUpdatePayload(values: AppointmentFormValues) {
  return {
    appointment_type: values.appointmentType,
    priority: values.priority,
    reason: values.reason,
    notes: values.notes,
    is_virtual: values.isVirtual,
    meeting_url: values.meetingUrl,
  };
}

export async function createAppointmentRequest(
  values: AppointmentFormValues,
  idempotencyKey = "",
): Promise<Appointment> {
  const { data } = await apiClient.post<AppointmentDto>(
    appointmentEndpoints.collection,
    toCreatePayload(values),
    idempotencyKey
      ? { headers: { "Idempotency-Key": idempotencyKey } }
      : undefined,
  );

  return mapAppointment(data);
}

async function createAppointment(values: AppointmentFormValues): Promise<Appointment> {
  return createAppointmentRequest(values);
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
      toUpdatePayload(values),
    );

  return mapAppointment(data);
}

async function rescheduleAppointment({
  id,
  values,
}: {
  id: string;
  values: Pick<AppointmentFormValues, "scheduledStart" | "scheduledEnd" | "durationMinutes">;
}): Promise<Appointment> {
  const { data } = await apiClient.post<AppointmentDto>(
    appointmentEndpoints.reschedule(id),
    {
      scheduled_start: new Date(values.scheduledStart).toISOString(),
      scheduled_end: new Date(values.scheduledEnd).toISOString(),
      duration_minutes: values.durationMinutes,
    },
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

export type AppointmentDepositCheckout = {
  key_id: string;
  order_id: string;
  amount: number;
  currency: string;
  invoice_id: string;
};

export type AppointmentCheckInResult = {
  appointment: Appointment;
  transcription_session: {
    session_id: string;
    status: string;
  } | null;
};

export async function checkInAppointment({
  appointmentId,
  recordingConsent,
}: {
  appointmentId: string;
  recordingConsent: boolean;
}): Promise<AppointmentCheckInResult> {
  const { data } = await apiClient.post<{
    appointment: AppointmentDto;
    transcription_session: AppointmentCheckInResult["transcription_session"];
  }>(appointmentEndpoints.checkIn(appointmentId), {
    recording_consent: recordingConsent,
  });
  return {
    appointment: mapAppointment(data.appointment),
    transcription_session: data.transcription_session,
  };
}

export async function createAppointmentDepositCheckout(
  appointmentId: string,
): Promise<AppointmentDepositCheckout> {
  const { data } = await apiClient.post<AppointmentDepositCheckout>(
    appointmentEndpoints.depositCheckout(appointmentId),
  );
  return data;
}

export async function markAppointmentNoShow(
  appointmentId: string,
): Promise<Appointment> {
  const { data } = await apiClient.post<AppointmentDto>(
    appointmentEndpoints.noShow(appointmentId),
  );
  return mapAppointment(data);
}

export async function verifyAppointmentDeposit({
  appointmentId,
  response,
}: {
  appointmentId: string;
  response: {
    razorpay_order_id: string;
    razorpay_payment_id: string;
    razorpay_signature: string;
  };
}): Promise<Appointment> {
  const { data } = await apiClient.post<AppointmentDto>(
    appointmentEndpoints.depositVerify(appointmentId),
    response,
  );
  return mapAppointment(data);
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

  reschedule: () =>
    mutationOptions({
      mutationFn: rescheduleAppointment,
    }),

  delete: () =>
    mutationOptions({
      mutationFn:
        deleteAppointment,
    }),
} as const;
