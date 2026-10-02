"use client";

import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import {
  patientKeys,
  patientMutations,
} from "../api";

export function useCreatePatientMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...patientMutations.create(),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey:
          patientKeys.lists(),
      });
    },
  });
}

export function useUpdatePatientMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...patientMutations.update(),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey:
          patientKeys.lists(),
      });

      queryClient.invalidateQueries({
        queryKey:
          patientKeys.detail(
            variables.id,
          ),
      });
    },
  });
}

export function useDeletePatientMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...patientMutations.delete(),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey:
          patientKeys.lists(),
      });
    },
  });
}
