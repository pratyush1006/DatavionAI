"use client";

/**
 * Organization mutation hooks.
 */

import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import {
  organizationKeys,
  organizationMutations,
} from "../api";

export function useCreateOrganizationMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    ...organizationMutations.create(),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: organizationKeys.lists(),
      });
    },
  });
}

export function useUpdateOrganizationMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    ...organizationMutations.update(),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: organizationKeys.lists(),
      });

      queryClient.invalidateQueries({
        queryKey: organizationKeys.detail(
          variables.id,
        ),
      });
    },
  });
}

export function useDeleteOrganizationMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    ...organizationMutations.delete(),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: organizationKeys.lists(),
      });
    },
  });
}
