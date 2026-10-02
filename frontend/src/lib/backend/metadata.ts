/**
 * DatavionOS metadata compatibility facade.
 *
 * This file preserves the existing consumer API while using the canonical
 * shared frontend types and backend runtime contracts.
 */

import { apiGet } from "@/lib/backend/http";
import { ENDPOINTS } from "@/lib/backend/endpoints";
import {
  getCities as canonicalGetCities,
  getCountries as canonicalGetCountries,
  getRegions as canonicalGetRegions,
} from "@/lib/backend/geography";
import type {
  DashboardConfig,
  LocationOption,
  OrganizationMetadata,
  SelectOption,
} from "@/lib/backend/types";

function normalizeOption(
  value: unknown,
  fallbackValue = "",
): SelectOption {
  if (typeof value === "string") {
    return {
      value: value || fallbackValue,
      label: value,
    };
  }

  if (!value || typeof value !== "object") {
    return {
      value: fallbackValue,
      label: fallbackValue,
    };
  }

  const record = value as Record<string, unknown>;
  const rawValue =
    record.value ??
    record.id ??
    record.code ??
    record.key ??
    fallbackValue;

  const rawLabel =
    record.label ??
    record.name ??
    record.display_name ??
    record.title ??
    record.code ??
    rawValue;

  return {
    value: String(rawValue ?? ""),
    label: String(rawLabel ?? ""),
    metadata: record,
  };
}

function normalizeLocation(
  value: unknown,
  level: LocationOption["level"],
  parentValue?: string,
): LocationOption {
  const option = normalizeOption(value);

  return {
    ...option,
    level,
    parentValue,
  };
}

export async function getOrganizationMetadata(): Promise<OrganizationMetadata> {
  const response = await apiGet<unknown>(ENDPOINTS.onboarding.catalog);
  const root =
    response.data && typeof response.data === "object"
      ? (response.data as Record<string, unknown>)
      : {};

  return {
    categories: Array.isArray(root.categories)
      ? root.categories.map((value) => normalizeOption(value))
      : [],
    types: Array.isArray(root.types)
      ? root.types.map((value) => normalizeOption(value))
      : [],
    sizes: Array.isArray(root.sizes)
      ? root.sizes.map((value) => normalizeOption(value))
      : [],
    departments: Array.isArray(root.departments)
      ? root.departments.map((value) => normalizeOption(value))
      : [],
    modules: Array.isArray(root.modules)
      ? root.modules.map((value) => normalizeOption(value))
      : [],
  };
}

export async function getCountries(): Promise<LocationOption[]> {
  const values = await canonicalGetCountries();
  return values.map((value) => normalizeLocation(value, "country"));
}

export const fetchCountries = getCountries;

export async function getStates(
  country: string,
): Promise<LocationOption[]> {
  const values = await canonicalGetRegions(country);
  return values.map((value) =>
    normalizeLocation(value, "state", country),
  );
}

export async function getDistricts(
  state: string,
): Promise<LocationOption[]> {
  /*
   * The canonical geography contract currently exposes region -> city.
   * Preserve this compatibility export by resolving cities for the supplied
   * region/state reference rather than introducing a legacy district API.
   */
  const values = await canonicalGetCities(state);
  return values.map((value) =>
    normalizeLocation(value, "district", state),
  );
}

export async function getCities(
  districtOrRegion: string,
): Promise<LocationOption[]> {
  const values = await canonicalGetCities(districtOrRegion);
  return values.map((value) =>
    normalizeLocation(value, "city", districtOrRegion),
  );
}

export async function getDashboardConfig(): Promise<DashboardConfig> {
  const response = await apiGet<unknown>(
    ENDPOINTS.runtime.bootstrap,
  );

  const root =
    response.data && typeof response.data === "object"
      ? (response.data as Record<string, unknown>)
      : {};

  const organization =
    root.organization && typeof root.organization === "object"
      ? (root.organization as Record<string, unknown>)
      : {};

  const subscription =
    root.subscription && typeof root.subscription === "object"
      ? (root.subscription as Record<string, unknown>)
      : null;

  const subscriptionPlan =
    subscription &&
    subscription.plan &&
    typeof subscription.plan === "object"
      ? (subscription.plan as Record<string, unknown>)
      : {};

  const user =
    root.user && typeof root.user === "object"
      ? (root.user as Record<string, unknown>)
      : {};

  const rawModules = Array.isArray(root.modules) ? root.modules : [];
  const rawDashboard = Array.isArray(root.dashboard) ? root.dashboard : [];

  const modules = rawModules.map((value) => {
    const moduleDefinition =
      value && typeof value === "object"
        ? (value as Record<string, unknown>)
        : {};

    const identifier = String(
      moduleDefinition.identifier ??
        moduleDefinition.key ??
        moduleDefinition.code ??
        moduleDefinition.name ??
        "",
    );

    return {
      key: identifier,
      name: String(
        moduleDefinition.display_name ??
          moduleDefinition.name ??
          identifier,
      ),
      description:
        typeof moduleDefinition.description === "string"
          ? moduleDefinition.description
          : undefined,
      department:
        typeof moduleDefinition.category === "string"
          ? moduleDefinition.category
          : undefined,
      enabled: moduleDefinition.enabled !== false,
      visible: moduleDefinition.enabled !== false,
      permissions: Array.isArray(moduleDefinition.permissions)
        ? moduleDefinition.permissions.map(String)
        : [],
      route:
        typeof moduleDefinition.route === "string"
          ? moduleDefinition.route
          : undefined,
    };
  });

  const quickActions = rawDashboard
    .map((value) => {
      const item =
        value && typeof value === "object"
          ? (value as Record<string, unknown>)
          : {};

      const key = String(item.key ?? item.route ?? "");
      const label = String(
        item.title ??
          item.label ??
          item.name ??
          key,
      );
      const href = String(item.route ?? "#");

      if (!key || !href) {
        return null;
      }

      return {
        key,
        label,
        href,
      };
    })
    .filter(
      (
        value,
      ): value is {
        key: string;
        label: string;
        href: string;
      } => value !== null,
    );

  return {
    organization: {
      id: String(organization.id ?? ""),
      name: String(organization.name ?? "Your workspace"),
      category:
        typeof organization.category === "string"
          ? organization.category
          : undefined,
      type:
        typeof organization.organization_type === "string"
          ? organization.organization_type
          : typeof organization.type === "string"
            ? organization.type
            : undefined,
      size:
        typeof organization.size === "string"
          ? organization.size
          : undefined,
    },
    subscription: {
      key: String(
        subscriptionPlan.code ??
          subscriptionPlan.key ??
          subscription?.status ??
          "",
      ),
      name: String(
        subscriptionPlan.name ??
          "Subscription",
      ),
      status:
        typeof subscription?.status === "string"
          ? subscription.status
          : undefined,
    },
    user: {
      id: String(user.id ?? ""),
      name:
        typeof user.name === "string"
          ? user.name
          : typeof user.full_name === "string"
            ? user.full_name
            : undefined,
      email:
        typeof user.email === "string"
          ? user.email
          : undefined,
    },
    modules,
    quickActions,
  };
}
