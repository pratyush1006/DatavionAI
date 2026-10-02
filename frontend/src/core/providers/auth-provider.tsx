"use client";

import {
  createContext,
  useContext,
  useMemo,
  type PropsWithChildren,
} from "react";
import type { AuthRuntime } from "../runtime/auth-types";
import { createAuthRuntime } from "../runtime/auth-runtime";

type AuthContextValue = AuthRuntime;

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({
  children,
  refreshBootstrap,
}: PropsWithChildren<{
  refreshBootstrap: () => Promise<void>;
}>) {
  const runtime = useMemo(
    () => createAuthRuntime(refreshBootstrap),
    [refreshBootstrap],
  );

  return (
    <AuthContext.Provider value={runtime}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
