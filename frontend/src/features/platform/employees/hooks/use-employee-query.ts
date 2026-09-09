/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/hooks/use-employee-query.ts
 * =============================================================================
 */

"use client";

import { useQuery } from "@tanstack/react-query";

import { employeeQueries } from "../api";

export function useEmployeeQuery(
  id: string,
) {
  return useQuery(
    employeeQueries.detail(id),
  );
}
