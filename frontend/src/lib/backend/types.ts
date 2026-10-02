export type SelectOption = {
  value: string;
  label: string;
  metadata?: Record<string, unknown>;
};

export type OrganizationMetadata = {
  categories: SelectOption[];
  types: SelectOption[];
  sizes: SelectOption[];
  departments?: SelectOption[];
  modules?: SelectOption[];
};

export type LocationOption = SelectOption & {
  level?: "country" | "state" | "district" | "city" | "postal_code";
  parentValue?: string;
};

export type DashboardConfig = {
  organization: {
    id: string;
    name: string;
    category?: string;
    type?: string;
    size?: string;
  };
  subscription: {
    key: string;
    name: string;
    status?: string;
  };
  user: {
    id: string;
    name?: string;
    email?: string;
  };
  modules: Array<{
    key: string;
    name: string;
    description?: string;
    department?: string;
    enabled: boolean;
    visible: boolean;
    permissions?: string[];
    route?: string;
  }>;
  quickActions?: Array<{
    key: string;
    label: string;
    href: string;
  }>;
  kpis?: Array<{
    key: string;
    label: string;
    value: string | number;
    trend?: string;
  }>;
};

export type BackendError = {
  detail?: string;
  message?: string;
  code?: string;
  [key: string]: unknown;
};
