/**
 * Organization query hook.
 */

"use client";

import { useQuery } from "@tanstack/react-query";

import { organizationQueries } from "../api";

export function useOrganizationQuery(
  id: number,
) {
  return useQuery(
    organizationQueries.detail(id),
  );
}
