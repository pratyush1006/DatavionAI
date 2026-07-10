/**
 * Logout mutation hook.
 */

"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";

import { accountKeys } from "../api/keys";
import { authService } from "../services/auth-service";

export function useLogoutMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      authService.logout();
    },

    onSuccess: () => {
      queryClient.removeQueries({
        queryKey: accountKeys.me(),
      });

      queryClient.clear();
    },
  });
}
