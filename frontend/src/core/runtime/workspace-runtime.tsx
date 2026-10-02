"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type PropsWithChildren,
} from "react";

import { useAuth } from "@/core/providers/auth-provider";
import type { WorkspaceRuntimeState } from "./workspace-types";

type BootstrapRefresh = () => Promise<void>;

const WorkspaceRuntimeContext =
  createContext<WorkspaceRuntimeState | null>(null);

function resolveBootstrapRefresh(): BootstrapRefresh {
  const globalObject = globalThis as typeof globalThis & {
    __DATAVION_BOOTSTRAP_REFRESH__?: BootstrapRefresh;
  };

  if (typeof globalObject.__DATAVION_BOOTSTRAP_REFRESH__ === "function") {
    return globalObject.__DATAVION_BOOTSTRAP_REFRESH__;
  }

  return async () => undefined;
}

export function WorkspaceRuntimeProvider({
  children,
}: PropsWithChildren) {
  const auth = useAuth();
  const [status, setStatus] =
    useState<WorkspaceRuntimeState["status"]>("loading");
  const [error, setError] = useState<Error | null>(null);

  const refresh = useCallback(async () => {
    setError(null);

    if (auth.session.status !== "authenticated") {
      setStatus(
        auth.session.status === "unknown"
          ? "loading"
          : "unauthenticated",
      );
      return;
    }

    try {
      setStatus("loading");
      await auth.refreshBootstrap();
      await resolveBootstrapRefresh()();
      setStatus("authenticated");
    } catch (cause) {
      const nextError =
        cause instanceof Error
          ? cause
          : new Error("Workspace bootstrap failed.");

      setError(nextError);
      setStatus("error");
    }
  }, [auth]);

  const logout = useCallback(async () => {
    try {
      await auth.logout();
    } finally {
      setError(null);
      setStatus("unauthenticated");
    }
  }, [auth]);

  useEffect(() => {
    const status = auth.session.status;

    if (status === "authenticated") {
      const timer = window.setTimeout(() => {
        void refresh();
      }, 0);

      return () => window.clearTimeout(timer);
    }

    if (status === "otp_required") {
      const timer = window.setTimeout(() => {
        setStatus("unauthenticated");
      }, 0);

      return () => window.clearTimeout(timer);
    }

    if (status === "unknown") {
      const timer = window.setTimeout(() => {
        setStatus("loading");
      }, 0);

      return () => window.clearTimeout(timer);
    }

    const timer = window.setTimeout(() => {
      setStatus("unauthenticated");
    }, 0);

    return () => window.clearTimeout(timer);
  }, [auth.session.status, refresh]);

  const value = useMemo<WorkspaceRuntimeState>(
    () => ({
      status,
      error,
      refresh,
      logout,
    }),
    [error, logout, refresh, status],
  );

  return (
    <WorkspaceRuntimeContext.Provider value={value}>
      {children}
    </WorkspaceRuntimeContext.Provider>
  );
}

export function useWorkspaceRuntime(): WorkspaceRuntimeState {
  const value = useContext(WorkspaceRuntimeContext);

  if (!value) {
    throw new Error(
      "useWorkspaceRuntime must be used inside WorkspaceRuntimeProvider.",
    );
  }

  return value;
}
