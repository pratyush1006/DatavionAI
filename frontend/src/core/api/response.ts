/**
 * =============================================================================
 * DatavionOS
 * File: src/core/api/response.ts
 * =============================================================================
 *
 * API response contract utilities.
 *
 * Responsibilities
 * ----------------
 * - Extract data from a validated API response
 * - Convert API error envelopes into ApiClientError
 *
 * This module intentionally contains no Axios or TanStack Query dependency.
 *
 * Design Principles
 * -----------------
 * - Framework independent
 * - Transport independent
 * - Strong TypeScript typing
 * - Single response utility ownership
 * - Enterprise Ready
 *
 * =============================================================================
 */

import {
  ApiClientError,
} from "./client";

import type {
  ApiResponse,
} from "@/core/types";

/* =============================================================================
 * Response Utilities
 * =============================================================================
 */

/**
 * Extract the business payload from a successful DatavionOS API response.
 *
 * ApiClient is responsible for:
 *
 * - HTTP status handling
 * - API envelope validation
 * - HTTP error normalization
 *
 * This helper operates on the API response contract itself.
 *
 * Because an ApiResponse does not contain HTTP status information, this
 * function does not invent one. HTTP status normalization belongs to ApiClient.
 *
 * @throws ApiClientError when the response represents an API error.
 */
export function unwrapData<T>(
  response: ApiResponse<T>,
): T {
  if (
    response.success === false
  ) {
    throw new ApiClientError(
      response.error,
      {
        statusCode: 0,
        meta: response.meta,
      },
    );
  }

  return response.data;
}
