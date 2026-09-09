/**
 * =============================================================================
 * DatavionOS
 * File: src/features/clinical/appointments/domain/types.ts
 * =============================================================================
 *
 * Appointment domain contracts.
 * =============================================================================
 */

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

export type AppointmentStatus =
  (typeof APPOINTMENT_STATUSES)[number];

export type AppointmentType =
  (typeof APPOINTMENT_TYPES)[number];

export type AppointmentPriority =
  (typeof APPOINTMENT_PRIORITIES)[number];

export type Appointment = {
  id: string;

  organization: string;

  patient: string;

  provider: string;

  appointmentNumber: string;

  appointmentType: AppointmentType;

  status: AppointmentStatus;

  priority: AppointmentPriority;

  scheduledStart: string;

  scheduledEnd: string;

  durationMinutes: number;

  reason: string;

  notes: string;

  isVirtual: boolean;

  meetingUrl: string;

  isActive: boolean;
};

export type AppointmentFormValues =
  Omit<Appointment, "id">;
