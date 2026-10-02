"use client";

import {
  useQuery,
} from "@tanstack/react-query";

import {
  appointmentQueries,
} from "../api";

export function useAppointmentsQuery() {
  return useQuery(
    appointmentQueries.all(),
  );
}

export function useAppointmentPatientsQuery() {
  return useQuery(appointmentQueries.patients());
}

export function useAppointmentProvidersQuery() {
  return useQuery(appointmentQueries.providers());
}
