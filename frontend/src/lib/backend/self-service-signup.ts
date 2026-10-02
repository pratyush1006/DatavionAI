import {
  apiEnvelope,
  apiPublicEnvelope,
} from "./http";

export type SelfServicePlan = {
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

export type SignupPreflight = {
  eligible: boolean;
  category: string;
  organization_type: string;
  size: string;
  plan: {
    id: string;
    code: string;
    name: string;
    price: string;
    currency: string;
    billing_cycle: string;
    trial_days: number;
  } | null;
  payment_required_now: boolean;
  payment_required_after_trial: boolean;
  next_step: string;
  errors: string[];
};

export type SignupRequest = {
  account: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
    phone?: string;
  };
  organization: {
    name: string;
    display_name?: string;
    code?: string;
    slug?: string;
    category: string;
    organization_type: string;
    size: string;
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
    plan_id: string;
    plan_code: string;
  };
};

export type SignupResult = {
  signup: {
    status: string;
    next_step: string;
    verification_required: boolean;
  };
  account: {
    user_id: string;
    email: string;
    email_verified: boolean;
  };
  organization: {
    id: string;
    name: string;
    display_name: string;
    code: string;
    slug: string;
    category?: string;
    organization_type: string;
    size?: string;
  };
  subscription: {
    id: string;
    status: string;
    plan: {
      id: string;
      code: string;
      name: string;
      healthcare_segment: string;
      billing_cycle: string;
      trial_days: number;
    };
  };
  modules: string[];
  features: string[];
  workspace: string;
  payment: {
    required_now: boolean;
    required_after_trial: boolean;
  };
};

export async function getSelfServicePlans(
  category: string,
  organizationType: string,
  size: string,
): Promise<SelfServicePlan[]> {
  const params = new URLSearchParams({
    category,
    organization_type: organizationType,
    size,
  });

  const response = await apiPublicEnvelope<SelfServicePlan[]>(
    `/onboarding/plans/?${params.toString()}`,
  );

  return response.data;
}

export async function preflightSelfServiceSignup(
  payload: {
    category: string;
    organization_type: string;
    size: string;
    plan_id?: string;
    plan_code?: string;
  },
): Promise<SignupPreflight> {
  const response = await apiEnvelope<SignupPreflight>(
    "/onboarding/signup/preflight/",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return response.data;
}

export async function submitSelfServiceSignup(
  payload: SignupRequest,
): Promise<SignupResult> {
  const response = await apiPublicEnvelope<SignupResult>(
    "/onboarding/signup/",
    {
      method: "POST",
      headers: {
        "Idempotency-Key": crypto.randomUUID(),
      },
      body: JSON.stringify(payload),
    },
  );

  return response.data;
}

export async function verifySignupEmail(
  email: string,
  otp: string,
): Promise<void> {
  await apiPublicEnvelope<null>(
    "/auth/verify-email/",
    {
      method: "POST",
      body: JSON.stringify({ email, otp }),
    },
  );
}

export async function resendSignupEmailOtp(
  email: string,
): Promise<void> {
  await apiPublicEnvelope<null>(
    "/auth/resend-verification/",
    {
      method: "POST",
      body: JSON.stringify({ email }),
    },
  );
}
