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
  "in_person",
  "virtual",
  "consultation",
  "follow_up",
  "emergency",
  "procedure",
] as const;

export const APPOINTMENT_PRIORITIES = [
  "routine",
  "urgent",
  "emergency",
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

  rescheduleCount: number;

  canReschedule: boolean;

  consultationFee: number;

  depositAmount: number;

  depositInvoiceId: string;

  finalInvoiceId: string;

  depositPaid: boolean;

  trackingToken: string;

  reason: string;

  notes: string;

  isVirtual: boolean;

  meetingUrl: string;

  isActive: boolean;
};

export type AppointmentFormValues = Pick<
  Appointment,
  | "patient"
  | "provider"
  | "appointmentNumber"
  | "appointmentType"
  | "priority"
  | "scheduledStart"
  | "scheduledEnd"
  | "durationMinutes"
  | "reason"
  | "notes"
  | "isVirtual"
  | "meetingUrl"
>;
