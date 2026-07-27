/**
 * Authentication mutations.
 */

import { apiClient } from "@/core/api";

import type {
  LoginRequest,
  LoginResponse,
} from "../domain/types";

import { accountEndpoints } from "./endpoints";

export async function login(
  payload: LoginRequest,
): Promise<LoginResponse> {
  const { data } = await apiClient.post(
    accountEndpoints.login,
    payload,
  );

  return data;
}
