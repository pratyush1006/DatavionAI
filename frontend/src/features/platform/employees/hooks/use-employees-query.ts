/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/hooks/use-employees-query.ts
 * =============================================================================
 */

"use client";

import { useQuery } from "@tanstack/react-query";

import { employeeQueries } from "../api";

export function useEmployeesQuery() {
  return useQuery(
    employeeQueries.all(),
  );
}
