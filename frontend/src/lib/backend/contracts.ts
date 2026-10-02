export type ApiEnvelope<T> = {
  success: boolean;
  message: string;
  data: T;
  meta?: {
    api_version?: string;
    timestamp?: string;
    request_id?: string;
    tenant_id?: string;
    pagination?: {
      count: number;
      page: number;
      page_size: number;
      total_pages: number;
      next: string | null;
      previous: string | null;
    };
    query?: Record<string, string>;
    [key: string]: unknown;
  };
};

export type OrganizationCatalogItem = {
  code: string;
  name: string;
};

export type OrganizationTypeCatalogItem = {
  code: string;
  name: string;
  category: string;
  category_name: string;
};

export type OrganizationCatalog = {
  categories: OrganizationCatalogItem[];
  types: OrganizationTypeCatalogItem[];
  sizes: OrganizationCatalogItem[];
};

export type SaaSPlan = {
  id: string;
  code: string;
  name: string;
  description: string;
  plan_type: string;
  healthcare_segment: string;
  price: string;
  currency: string;
  billing_cycle: string;
  trial_days: number;
  modules: unknown;
  features: unknown;
  limits: unknown;
  is_featured: boolean;
  is_default: boolean;
};

export type GeographyCountry = {
  id: string;
  code: string;
  name: string;
  iso3: string;
  phone_code: string;
};

export type GeographyRegion = {
  id: string;
  country: string;
  code: string;
  name: string;
  region_type: string;
};

export type GeographyCity = {
  id: string;
  country: string;
  region: string;
  name: string;
  latitude: string | number | null;
  longitude: string | number | null;
  timezone: string | null;
};

export type CurrentLocationResult = {
  latitude: number;
  longitude: number;
  accuracy_meters: number | null;
  formatted_address: string;
  country: string;
  country_code: string;
  state: string;
  district: string;
  city: string;
    postal_code: string;
    timezone: string;
    provider: string;
  reference: Record<string, unknown>;
};

export type AuthUser = {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
};

export type LoginChallenge = {
  otp_id: string;
  requires_otp: boolean;
  expires_at: string;
  resend_available_at?: string;
};

export type TokenPair = {
  access: string;
  refresh: string;
};

export type TenantBootstrap = {
  id: string;
  name: string;
  tenant_type: string;
  status: string;
};

export type PlatformBootstrap = {
  user: AuthUser;
  tenant: TenantBootstrap | null;
  organization: {
    id: string;
    name: string;
  } | null;
  employee: {
    id: string;
    employee_code: string;
  } | null;
  platform_roles: string[];
  organization_roles: string[];
  permissions: string[];
  modules: Array<{
    identifier: string;
    name: string;
    display_name: string;
    description: string;
    version: string;
    category: string;
    route: string;
    api_prefix: string;
    icon: string;
    permissions: string[];
    enabled: boolean;
    system: boolean;
    tenant_scoped: boolean;
    order: number;
    tags: string[];
    feature_flags: string[];
  }>;
  navigation: Array<{
    title: string;
    route: string;
    icon: string;
    category: string;
    permissions: string[];
    order: number;
  }>;
  dashboard: Array<{
    key: string;
    title: string;
    description: string;
    icon: string;
    route: string;
    category: string;
    order: number;
  }>;
  branding: Record<string, unknown>;
  feature_flags: Record<string, unknown>;
  subscription: {
    status: string;
    auto_renew: boolean;
    plan: {
      name: string;
      code: string;
      billing_cycle: string;
    };
  } | null;
  preferences: Record<string, unknown> | null;
};

export type OrganizationRegistrationPayload = {
  name: string;
  display_name?: string;
  code?: string;
  slug?: string;
  organization_type: string;
  category?: string;
  category_name?: string;
  size?: string;
  email?: string;
  support_email?: string;
  phone?: string;
  website?: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  country_ref?: string | null;
  region_ref?: string | null;
  city_ref?: string | null;
  postal_code?: string;
  timezone?: string;
  registration_number?: string;
  tax_number?: string;
  license_number?: string;
  accreditation?: string;
  description?: string;
  is_demo?: boolean;
  plan_id?: string | null;
  plan_code?: string;
};

export type OrganizationOnboardingResult = {
  organization: {
    id: string;
    name: string;
    display_name: string;
    code: string;
    slug: string;
    organization_type: string;
  };
  subscription: {
    id: string;
    status: string;
    plan: {
      id: string;
      code: string;
      name: string;
      healthcare_segment: string;
    };
  };
  modules: string[];
  features: string[];
  workspace: string;
  created_organization: boolean;
  created_subscription: boolean;
  organization_admin_assigned: boolean;
};

export type OrganizationOnboardingStatusItem = {
  organization: {
    id: string;
    name: string;
    display_name: string;
    code: string;
    slug: string;
    organization_type: string;
  };
  subscription: {
    id: string;
    status: string;
    plan: {
      id: string;
      code: string;
      name: string;
      healthcare_segment: string;
    };
  } | null;
  organization_admin: boolean;
  workspace: string;
};

export type RegisterUserPayload = {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  organization_name: string;
  organization_type: string;
};

export type OrganizationControlPlaneSnapshot = {
  organization: {
    id: string;
    name: string;
    display_name: string;
    code: string;
    organization_type: string;
    status: string;
    is_active: boolean;
  };
  subscription: Record<string, unknown> | null;
  modules: Array<{
    id: string;
    module_code: string;
    status: string;
    settings: Record<string, unknown>;
    enabled_at: string | null;
    disabled_at: string | null;
  }>;
  features: Array<{
    id: string;
    feature_code: string;
    feature_name: string | null;
    status: string;
    configuration: Record<string, unknown>;
    enabled_at: string | null;
    disabled_at: string | null;
  }>;
  can_manage_modules: boolean;
  can_manage_features: boolean;
};

export type OrganizationCapabilityTogglePayload = {
  enabled: boolean;
};
