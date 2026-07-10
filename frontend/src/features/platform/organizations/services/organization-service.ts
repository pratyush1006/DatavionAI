/**
 * Organization service.
 *
 * Business orchestration layer for organization operations.
 *
 * Responsibilities:
 * - Normalize payloads before sending to the API.
 * - Encapsulate organization-specific business rules.
 * - Orchestrate multiple business operations when required.
 *
 * This layer must NOT:
 * - Make HTTP requests.
 * - Use React Query hooks.
 * - Contain UI logic.
 */

import type {
  CreateOrganizationPayload,
  UpdateOrganizationPayload,
} from "../domain";

import {
  organizationMutations,
  organizationQueries,
} from "../api";

export const organizationService = {
  /**
   * Query definitions.
   */
  queries: organizationQueries,

  /**
   * Mutation definitions.
   */
  mutations: organizationMutations,

  /**
   * Prepare organization payload before creation.
   */
  prepareCreatePayload(
    payload: CreateOrganizationPayload,
  ): CreateOrganizationPayload {
    return {
      ...payload,
      name: payload.name.trim(),
      code: payload.code.trim().toUpperCase(),
      email: payload.email.trim(),
      phone: payload.phone.trim(),
      address: payload.address.trim(),
      city: payload.city.trim(),
      state: payload.state.trim(),
      country: payload.country.trim(),
    };
  },

  /**
   * Prepare organization payload before update.
   *
   * Organization code is immutable and therefore
   * is not part of the update payload.
   */
  prepareUpdatePayload(
    payload: UpdateOrganizationPayload,
  ): UpdateOrganizationPayload {
    return {
      ...payload,
      name: payload.name.trim(),
      email: payload.email.trim(),
      phone: payload.phone.trim(),
      address: payload.address.trim(),
      city: payload.city.trim(),
      state: payload.state.trim(),
      country: payload.country.trim(),
    };
  },

  /**
   * Returns whether the organization is active.
   */
  isOrganizationActive(
    isActive: boolean,
  ): boolean {
    return isActive;
  },
} as const;
