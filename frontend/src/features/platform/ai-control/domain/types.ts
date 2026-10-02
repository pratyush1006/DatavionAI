export interface AICapability {
  id: string;
  code: string;
  name: string;
  department: string;
  status: string;
  organization_enabled: boolean;
  entitled: boolean;
  module_enabled: boolean;
  feature_enabled: boolean;
  user_permission: boolean;
  department_access: boolean;
  can_use: boolean;
  required_module: string;
  required_feature: string;
  required_permission: string;
  human_review_required: boolean;
  governance: Record<string, unknown>;
}

export interface AIControlSnapshot {
  organization: {
    id: string;
    name: string;
    code: string;
  };
  capabilities: AICapability[];
  can_manage_ai: boolean;
}
