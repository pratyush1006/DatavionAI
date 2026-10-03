/**
 * =============================================================================
 * DatavionOS
 * File:
 * src/features/platform/onboarding/domain/contracts.ts
 * =============================================================================
 *
 * Canonical Organization Onboarding domain contracts.
 * =============================================================================
 */

export interface OrganizationCategoryOption {
  readonly code: string;
  readonly name: string;
}

export interface OrganizationTypeOption {
  readonly code: string;
  readonly name: string;
  readonly category: string;
}

export interface OrganizationSizeOption {
  readonly code: string;
  readonly name: string;
}

export interface OrganizationCatalog {
  readonly categories: readonly OrganizationCategoryOption[];
  readonly types: readonly OrganizationTypeOption[];
  readonly sizes: readonly OrganizationSizeOption[];
}

export interface SaaSPlan {
  readonly id: string;
  readonly code: string;
  readonly name: string;
  readonly description: string;
  readonly plan_type: string;
  readonly healthcare_segment: string;
  readonly price: string | number;
  readonly currency: string;
  readonly billing_cycle: string;
  readonly trial_days: number;
  readonly modules: Readonly<Record<string, boolean>>;
  readonly features: Readonly<Record<string, boolean>>;
  readonly limits: Readonly<Record<string, unknown>>;
  readonly is_featured: boolean;
  readonly is_default: boolean;
}

export interface OrganizationRegistrationPayload {
  readonly name: string;
  readonly display_name?: string;
  readonly code?: string;
  readonly slug?: string;
  readonly organization_type: string;
  readonly category?: string;
  readonly size?: string;
  readonly email?: string;
  readonly support_email?: string;
  readonly phone?: string;
  readonly website?: string;
  readonly address?: string;
  readonly city?: string;
  readonly state?: string;
  readonly country?: string;
  readonly postal_code?: string;
  readonly timezone?: string;
  readonly registration_number?: string;
  readonly tax_number?: string;
  readonly license_number?: string;
  readonly accreditation?: string;
  readonly description?: string;
  readonly is_demo?: boolean;
  readonly plan_code?: string;
}

export interface OrganizationOnboardingResult {
  readonly organization: {
    readonly id: string;
    readonly name: string;
    readonly display_name: string;
    readonly code: string;
    readonly slug: string;
    readonly organization_type: string;
  };

  readonly subscription: {
    readonly id: string;
    readonly status: string;
    readonly plan: {
      readonly id: string;
      readonly code: string;
      readonly name: string;
      readonly healthcare_segment: string;
    };
  };

  readonly modules: readonly string[];
  readonly features: readonly string[];
  readonly workspace: string;
  readonly created_organization: boolean;
  readonly created_subscription: boolean;
  readonly organization_admin_assigned: boolean;
}

export interface OrganizationOnboardingStatusItem {
  readonly organization:
    OrganizationOnboardingResult["organization"];

  readonly subscription:
    OrganizationOnboardingResult["subscription"] | null;

  readonly organization_admin: boolean;
  readonly workspace: string;
}