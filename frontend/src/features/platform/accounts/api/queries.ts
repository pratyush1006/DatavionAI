/**
 * Authentication queries.
 */

import { queryOptions } from "@tanstack/react-query";

import { apiClient } from "@/core/api";

import type { User } from "../domain/types";

import { accountEndpoints } from "./endpoints";
import { accountKeys } from "./keys";

export const accountQueries = {
  me() {
    return queryOptions({
      queryKey: accountKeys.me(),

      queryFn: async (): Promise<User> => {
        const { data } = await apiClient.get(
          accountEndpoints.me,
        );

        return data;
      },
    });
  },
};
