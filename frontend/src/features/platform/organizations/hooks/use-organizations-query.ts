"use client";

import { useQuery } from "@tanstack/react-query";

import { organizationQueries } from "../api";

export function useOrganizationsQuery() {
  return useQuery(
    organizationQueries.all(),
  );
}
