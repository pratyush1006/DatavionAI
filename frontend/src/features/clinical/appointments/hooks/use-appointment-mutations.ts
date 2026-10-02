"use client";

import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import {
  appointmentKeys,
  appointmentMutations,
  checkInAppointment,
  markAppointmentNoShow,
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

export function useRescheduleAppointmentMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    ...appointmentMutations.reschedule(),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: appointmentKeys.lists(),
      });
      queryClient.invalidateQueries({
        queryKey: appointmentKeys.detail(variables.id),
      });
    },
  });
}

export function useCheckInAppointmentMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: checkInAppointment,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: appointmentKeys.lists(),
      });
    },
  });
}

export function useNoShowAppointmentMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: markAppointmentNoShow,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: appointmentKeys.lists(),
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
