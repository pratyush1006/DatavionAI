/**
 * Shared API client.
 */

import axios from "axios";

import { env } from "@/core/config/env";

export const apiClient = axios.create({
  baseURL: env.apiBaseUrl,

  timeout: 30_000,

  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});
