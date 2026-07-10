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
  console.log("LOGIN PAYLOAD:", payload);

  try {
    const { data } = await apiClient.post(
      accountEndpoints.login,
      payload,
    );

    console.log("LOGIN RESPONSE:", data);

    return data;
  } catch (error) {
    console.error("LOGIN ERROR:", error);

    throw error;
  }
}
