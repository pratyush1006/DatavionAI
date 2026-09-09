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
