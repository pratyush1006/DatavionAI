/**
 * Current user query hook.
 */

"use client";

import { useQuery } from "@tanstack/react-query";

import { accountQueries } from "../api/queries";
import { authStorage } from "../services/auth-storage";

export function useMeQuery() {
  const enabled =
    typeof window !== "undefined" &&
    !!authStorage.getAccessToken();

  return useQuery({
    ...accountQueries.me(),

    enabled,
  });
}
