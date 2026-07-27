import { apiClient } from "@/core/api";

export const APPOINTMENT_STATUSES = [
  "scheduled",
  "confirmed",
  "checked_in",
  "in_progress",
  "completed",
  "cancelled",
  "no_show",
] as const;

export const APPOINTMENT_TYPES = [
  "consultation",
  "follow_up",
  "emergency",
  "surgery",
  "procedure",
  "teleconsultation",
] as const;

export const APPOINTMENT_PRIORITIES = [
  "low",
  "normal",
  "high",
  "urgent",
] as const;

export type Appointment = {
  id: string;
  organization: string;
  patient: string;
  provider: string;
  appointmentNumber: string;
  appointmentType: (typeof APPOINTMENT_TYPES)[number];
  status: (typeof APPOINTMENT_STATUSES)[number];
  priority: (typeof APPOINTMENT_PRIORITIES)[number];
  scheduledStart: string;
  scheduledEnd: string;
  durationMinutes: number;
  reason: string;
  notes: string;
  isVirtual: boolean;
  meetingUrl: string;
  isActive: boolean;
};

export type AppointmentFormValues = Omit<Appointment, "id">;

type AppointmentDto = Record<string, unknown>;
type ListResponse = { data: AppointmentDto[] };

function mapAppointment(dto: AppointmentDto): Appointment {
  return {
    id: String(dto.id),
    organization: String(dto.organization),
    patient: String(dto.patient),
    provider: String(dto.provider),
    appointmentNumber: String(dto.appointment_number),
    appointmentType: dto.appointment_type as Appointment["appointmentType"],
    status: dto.status as Appointment["status"],
    priority: dto.priority as Appointment["priority"],
    scheduledStart: String(dto.scheduled_start),
    scheduledEnd: String(dto.scheduled_end),
    durationMinutes: Number(dto.duration_minutes),
    reason: String(dto.reason ?? ""),
    notes: String(dto.notes ?? ""),
    isVirtual: Boolean(dto.is_virtual),
    meetingUrl: String(dto.meeting_url ?? ""),
    isActive: Boolean(dto.is_active),
  };
}

function toPayload(values: AppointmentFormValues) {
  return {
    organization: values.organization,
    patient: values.patient,
    provider: values.provider,
    appointment_number: values.appointmentNumber,
    appointment_type: values.appointmentType,
    status: values.status,
    priority: values.priority,
    scheduled_start: values.scheduledStart,
    scheduled_end: values.scheduledEnd,
    duration_minutes: values.durationMinutes,
    reason: values.reason,
    notes: values.notes,
    is_virtual: values.isVirtual,
    meeting_url: values.meetingUrl,
    is_active: values.isActive,
  };
}

export async function fetchAppointments() {
  const { data } = await apiClient.get<ListResponse>("/appointments/");
  return data.data.map(mapAppointment);
}

export async function createAppointment(values: AppointmentFormValues) {
  const { data } = await apiClient.post<AppointmentDto>(
    "/appointments/",
    toPayload(values),
  );

  return mapAppointment(data);
}

export async function updateAppointment({
  id,
  values,
}: {
  id: string;
  values: AppointmentFormValues;
}) {
  const { data } = await apiClient.patch<AppointmentDto>(
    `/appointments/${id}/`,
    toPayload(values),
  );

  return mapAppointment(data);
}

export async function deleteAppointment(id: string) {
  await apiClient.delete(`/appointments/${id}/`);
}
