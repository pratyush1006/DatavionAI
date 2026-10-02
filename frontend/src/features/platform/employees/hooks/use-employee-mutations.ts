/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/hooks/use-employee-mutations.ts
 * =============================================================================
 *
 * Employee mutation hooks.
 *
 * Query invalidation is centralized here so UI components do not need to know
 * how the Employee query cache is structured.
 * =============================================================================
 */

"use client";

import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import {
  employeeKeys,
  employeeMutations,
} from "../api";

export function useCreateEmployeeMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...employeeMutations.create(),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.lists(),
      });
    },
  });
}

export function useUpdateEmployeeMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...employeeMutations.update(),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.lists(),
      });

      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.detail(
            variables.id,
          ),
      });
    },
  });
}

export function useDeleteEmployeeMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...employeeMutations.delete(),

    onSuccess: (_, id) => {
      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.lists(),
      });

      queryClient.removeQueries({
        queryKey:
          employeeKeys.detail(id),
      });
    },
  });
}

export function useActivateEmployeeMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...employeeMutations.activate(),

    onSuccess: (_, id) => {
      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.lists(),
      });

      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.detail(id),
      });
    },
  });
}

export function useDeactivateEmployeeMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...employeeMutations.deactivate(),

    onSuccess: (_, id) => {
      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.lists(),
      });

      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.detail(id),
      });
    },
  });
}

export function useEmployeeAssignmentMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...employeeMutations.assignment(),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.lists(),
      });

      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.detail(
            variables.id,
          ),
      });
    },
  });
}

export function useEmployeeContractMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...employeeMutations.contract(),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.lists(),
      });

      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.detail(
            variables.id,
          ),
      });
    },
  });
}

export function useEmployeeOnboardingMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...employeeMutations.onboard(),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.lists(),
      });
    },
  });
}

export function useEmployeeOffboardingMutation() {
  const queryClient =
    useQueryClient();

  return useMutation({
    ...employeeMutations.offboard(),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.lists(),
      });

      queryClient.invalidateQueries({
        queryKey:
          employeeKeys.detail(
            variables.id,
          ),
      });
    },
  });
}
