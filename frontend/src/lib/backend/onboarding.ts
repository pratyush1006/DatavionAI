
/**
 * Canonical DatavionOS onboarding contract.
 */

import {
  apiPublicGet,
} from "./http";
import { ENDPOINTS } from "@/lib/backend/endpoints";

export type OrganizationCatalogItem = {
  id: string;
  code: string;
  name: string;
  [key: string]: unknown;
};

export type OrganizationCatalogType = OrganizationCatalogItem & {
  category?: string | null;
  category_name?: string | null;
};

export type OrganizationCatalog = {
  categories: OrganizationCatalogItem[];
  types: OrganizationCatalogType[];
  sizes: OrganizationCatalogItem[];
};

export async function fetchOrganizationCatalog(): Promise<OrganizationCatalog> {
  const response = await apiPublicGet<OrganizationCatalog>(ENDPOINTS.onboarding.catalog);
  return response.data;
}

export const getOrganizationCatalog = fetchOrganizationCatalog;
