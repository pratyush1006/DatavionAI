"use client";

import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import {
  appointmentKeys,
  appointmentMutations,
} from "../api";

export function useCreateAppointmentMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...appointmentMutations.create(),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey:
          appointmentKeys.lists(),
      });
    },
  });
}

export function useUpdateAppointmentMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...appointmentMutations.update(),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey:
          appointmentKeys.lists(),
      });

      queryClient.invalidateQueries({
        queryKey:
          appointmentKeys.detail(
            variables.id,
          ),
      });
    },
  });
}

export function useDeleteAppointmentMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...appointmentMutations.delete(),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey:
          appointmentKeys.lists(),
      });
    },
  });
}
