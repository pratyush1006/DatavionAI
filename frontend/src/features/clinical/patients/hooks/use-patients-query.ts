"use client";

import {
  useQuery,
} from "@tanstack/react-query";

import {
  patientQueries,
} from "../api";

export function usePatientsQuery() {
  return useQuery(
    patientQueries.all(),
  );
}
