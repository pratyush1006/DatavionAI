export type OrganizationCapabilityStatus =
  | "enabled"
  | "disabled"
  | "trial"
  | "locked"
  | string;

export interface OrganizationControlModule {
  id: string;
  module_code: string;
  status: OrganizationCapabilityStatus;
  settings: Record<string, unknown>;
  enabled_at: string | null;
  disabled_at: string | null;
}

export interface OrganizationControlFeature {
  id: string;
  feature_code: string;
  feature_name: string | null;
  status: OrganizationCapabilityStatus;
  configuration: Record<string, unknown>;
  enabled_at: string | null;
  disabled_at: string | null;
}

export interface OrganizationControlSubscription {
  id: string;
  status: string;
  plan: {
    id: string | null;
    name: string | null;
    code: string | null;
    healthcare_segment: string | null;
  };
  starts_at: string | null;
  ends_at: string | null;
}

export interface OrganizationControlPlaneSnapshot {
  organization: {
    id: string;
    name: string;
    display_name: string;
    code: string;
    organization_type: string;
    status: string;
    is_active: boolean;
  };
  subscription: OrganizationControlSubscription | null;
  modules: OrganizationControlModule[];
  features: OrganizationControlFeature[];
  can_manage_modules: boolean;
  can_manage_features: boolean;
}
