/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/organizations/hooks/use-organization-query.ts
 * =============================================================================
 *
 * Organization detail query hook.
 * =============================================================================
 */

"use client";

import {
  useQuery,
} from "@tanstack/react-query";

import {
  organizationQueries,
} from "../api";

export function useOrganizationQuery(
  id: string,
  enabled = true,
) {
  return useQuery(
    organizationQueries.detail(id, enabled),
  );
}
