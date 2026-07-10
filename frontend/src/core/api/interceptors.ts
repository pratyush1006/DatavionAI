/**
 * Axios interceptors.
 */

import type {
  AxiosError,
  InternalAxiosRequestConfig,
} from "axios";

import { apiClient } from "./client";

import { authStorage } from "@/features/platform/accounts/services/auth-storage";

let registered = false;

export function registerInterceptors(): void {
  if (registered) {
    return;
  }

  registered = true;

  apiClient.interceptors.request.use(
    (
      config: InternalAxiosRequestConfig,
    ) => {
      const token =
        authStorage.getAccessToken();

      if (token) {
        config.headers.Authorization =
          `Bearer ${token}`;
      }

      return config;
    },
  );

  apiClient.interceptors.response.use(
    (response) => response,

    (
      error: AxiosError,
    ) => {
      if (error.response?.status === 401) {
        authStorage.clear();

        if (
          typeof window !== "undefined"
        ) {
          window.location.replace(
            "/login",
          );
        }
      }

      return Promise.reject(error);
    },
  );
}
