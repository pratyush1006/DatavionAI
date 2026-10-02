import { apiClient } from "@/core/api";

export interface PublicSaaSPlan {
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
  readonly is_featured: boolean;
  readonly is_default: boolean;
}

export async function fetchPublicSaaSPlans(): Promise<PublicSaaSPlan[]> {
  const response = await apiClient.get<PublicSaaSPlan[]>("/onboarding/plans/");
  return response.data;
}
