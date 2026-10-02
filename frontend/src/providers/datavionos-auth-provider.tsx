"use client";

import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  clearSession,
  getSession,
  type AuthSession,
  type AuthUser,
  setSession,
} from "@/lib/datavionos/auth-runtime";

type AuthContextValue = {
  session: AuthSession;
  user: AuthUser | null;
  authenticated: boolean;
  loading: boolean;
  signIn: (
    accessToken: string,
    refreshToken: string | null,
    user: AuthUser | null,
  ) => void;
  signOut: () => void;
};

const AuthContext =
  createContext<AuthContextValue | null>(null);

export function DatavionOSAuthProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [session, setSessionState] =
    useState<AuthSession>({
      accessToken: null,
      refreshToken: null,
      user: null,
    });

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    const session = getSession();

    queueMicrotask(() => {
      setSessionState(session);
      setLoading(false);
    });
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      session,
      user: session.user,
      authenticated: Boolean(session.accessToken),
      loading,

      signIn: (
        accessToken,
        refreshToken,
        user,
      ) => {
        setSession(
          accessToken,
          refreshToken,
          user,
        );

        setSessionState({
          accessToken,
          refreshToken,
          user,
        });
      },

      signOut: () => {
        clearSession();

        setSessionState({
          accessToken: null,
          refreshToken: null,
          user: null,
        });
      },
    }),
    [session, loading],
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useDatavionOSAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useDatavionOSAuth must be used inside DatavionOSAuthProvider.",
    );
  }

  return context;
}
