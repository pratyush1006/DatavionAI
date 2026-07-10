/**
 * Organization mutations.
 */

import {
  mutationOptions,
} from "@tanstack/react-query";

import { apiClient } from "@/core/api";

import type {
  CreateOrganizationPayload,
  Organization,
  UpdateOrganizationPayload,
} from "../domain";

import {
  organizationEndpoints,
} from "./endpoints";

async function createOrganization(
  payload: CreateOrganizationPayload,
) {
  const { data } =
    await apiClient.post<Organization>(
      organizationEndpoints.collection,
      payload,
    );

  return data;
}

async function updateOrganization({
  id,
  payload,
}: {
  id: number | string;
  payload: UpdateOrganizationPayload;
}) {
  const { data } =
    await apiClient.patch<Organization>(
      organizationEndpoints.byId(id),
      payload,
    );

  return data;
}

async function deleteOrganization(
  id: number | string,
) {
  await apiClient.delete(
    organizationEndpoints.byId(id),
  );
}

export const organizationMutations = {
  create: () =>
    mutationOptions({
      mutationFn:
        createOrganization,
    }),

  update: () =>
    mutationOptions({
      mutationFn:
        updateOrganization,
    }),

  delete: () =>
    mutationOptions({
      mutationFn:
        deleteOrganization,
    }),
} as const;
