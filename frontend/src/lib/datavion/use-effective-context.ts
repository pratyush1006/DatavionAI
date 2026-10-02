"use client";

import { API_BASE_URL } from "@/core/api/config";
import { useEffect, useState } from "react";
import type { EffectiveCapabilityContext } from "./capabilities";

type State = { context: EffectiveCapabilityContext | null; loading: boolean; error: string | null };
const API_BASE = API_BASE_URL?.replace(/\/$/, "") ?? API_BASE_URL;

export function useEffectiveCapabilityContext(): State {
  const [state, setState] = useState<State>({ context: null, loading: true, error: null });
  useEffect(() => {
    let cancelled = false;
    async function load(): Promise<void> {
      try {
        const response = await fetch(`${API_BASE}/context/effective/`, {
          credentials: "include", headers: { Accept: "application/json" }, cache: "no-store",
        });
        if (!response.ok) throw new Error(`Effective context request failed: ${response.status}`);
        const context = (await response.json()) as EffectiveCapabilityContext;
        if (!cancelled) setState({ context, loading: false, error: null });
      } catch (error) {
        if (!cancelled) setState({ context: null, loading: false, error: error instanceof Error ? error.message : "Unknown error" });
      }
    }
    void load();
    return () => { cancelled = true; };
  }, []);
  return state;
}
