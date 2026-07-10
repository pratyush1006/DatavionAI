/**
 * Login mutation hook.
 */

"use client";

import { useMutation } from "@tanstack/react-query";

import { authService } from "../services/auth-service";

export function useLoginMutation() {
  return useMutation({
    mutationFn: authService.login.bind(authService),
  });
}
