"use client";

import type { ReactNode } from "react";

import { AuthContext } from "./auth-context";

import { useLogoutMutation } from "@/features/platform/accounts/hooks/use-logout-mutation";
import { useMeQuery } from "@/features/platform/accounts/hooks/use-me-query";

type Props = Readonly<{
  children: ReactNode;
}>;

export function AuthProvider({
  children,
}: Props) {
  const {
    data: user,
    isLoading,
  } = useMeQuery();

  const logoutMutation =
    useLogoutMutation();

  return (
    <AuthContext.Provider
      value={{
        user: user ?? null,

        isAuthenticated: !!user,

        isLoading,

        logout: () =>
          logoutMutation.mutate(),
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
