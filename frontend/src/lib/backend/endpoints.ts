const env = (key: string, fallback: string) =>
  process.env[key] || fallback;

export const ENDPOINTS = {
  auth: {
    register: env("NEXT_PUBLIC_API_AUTH_REGISTER", "/auth/register/"),
    login: env("NEXT_PUBLIC_API_AUTH_LOGIN", "/auth/login/"),
    resendLoginOtp: env(
      "NEXT_PUBLIC_API_AUTH_RESEND_LOGIN_OTP",
      "/auth/login/resend-otp/",
    ),
    verifyLoginOtp: env(
      "NEXT_PUBLIC_API_AUTH_VERIFY_LOGIN_OTP",
      "/auth/login/verify-otp/",
    ),
    refresh: env("NEXT_PUBLIC_API_AUTH_REFRESH", "/auth/refresh/"),
    logout: env("NEXT_PUBLIC_API_AUTH_LOGOUT", "/auth/logout/"),
    me: env("NEXT_PUBLIC_API_AUTH_ME", "/auth/me/"),
    forgotPassword: env(
      "NEXT_PUBLIC_API_AUTH_FORGOT_PASSWORD",
      "/auth/forgot-password/",
    ),
    resetPassword: env(
      "NEXT_PUBLIC_API_AUTH_RESET_PASSWORD",
      "/auth/reset-password/",
    ),
    changePassword: env(
      "NEXT_PUBLIC_API_AUTH_CHANGE_PASSWORD",
      "/auth/change-password/",
    ),
    verifyEmail: env(
      "NEXT_PUBLIC_API_AUTH_VERIFY_EMAIL",
      "/auth/verify-email/",
    ),
    resendVerification: env(
      "NEXT_PUBLIC_API_AUTH_RESEND_VERIFICATION",
      "/auth/resend-verification/",
    ),
    google: env(
      "NEXT_PUBLIC_API_AUTH_GOOGLE",
      "/auth/oauth/google/",
    ),
    microsoft: env(
      "NEXT_PUBLIC_API_AUTH_MICROSOFT",
      "/auth/oauth/microsoft/",
    ),
  },

  onboarding: {
    catalog: env("NEXT_PUBLIC_API_ONBOARDING_CATALOG", "/onboarding/catalog/"),
    organizationTypes: env(
      "NEXT_PUBLIC_API_ONBOARDING_ORGANIZATION_TYPES",
      "/onboarding/organization-types/",
    ),
    plans: env("NEXT_PUBLIC_API_ONBOARDING_PLANS", "/onboarding/plans/"),
    registerOrganization: env(
      "NEXT_PUBLIC_API_ONBOARDING_REGISTER",
      "/onboarding/register/",
    ),
    status: env(
      "NEXT_PUBLIC_API_ONBOARDING_STATUS",
      "/onboarding/status/",
    ),
  },

  geography: {
    countries: env(
      "NEXT_PUBLIC_API_GEOGRAPHY_COUNTRIES",
      "/geography/countries/",
    ),
    regions: env(
      "NEXT_PUBLIC_API_GEOGRAPHY_REGIONS",
      "/geography/regions/",
    ),
    cities: env(
      "NEXT_PUBLIC_API_GEOGRAPHY_CITIES",
      "/geography/cities/",
    ),
    currentLocation: env(
      "NEXT_PUBLIC_API_GEOGRAPHY_CURRENT_LOCATION",
      "/geography/current-location/",
    ),
  },

  tenancy: {
    myTenants: env("NEXT_PUBLIC_API_MY_TENANTS", "/tenancy/my-tenants/"),
    selectTenant: env("NEXT_PUBLIC_API_SELECT_TENANT", "/tenancy/select/"),
  },

  organizations: {
    listCreate: env(
      "NEXT_PUBLIC_API_ORGANIZATIONS",
      "/organizations/",
    ),
    byId: (organizationId: string) =>
      `${env("NEXT_PUBLIC_API_ORGANIZATIONS", "/organizations/")}${organizationId}/`,
  },

  runtime: {
    bootstrap: env(
      "NEXT_PUBLIC_API_PLATFORM_BOOTSTRAP",
      "/platform/bootstrap/",
    ),
  },

  controlPlane: {
    snapshot: env(
      "NEXT_PUBLIC_API_ORGANIZATION_CONTROL_PLANE",
      "/organization-control/",
    ),
    toggleModule: (moduleId: string) =>
      `${env("NEXT_PUBLIC_API_ORGANIZATION_CONTROL_PLANE", "/organization-control/")}modules/${moduleId}/`,
    toggleFeature: (featureId: string) =>
      `${env("NEXT_PUBLIC_API_ORGANIZATION_CONTROL_PLANE", "/organization-control/")}features/${featureId}/`,
  },

  accessControl: {
    snapshot: env(
      "NEXT_PUBLIC_API_ORGANIZATION_ACCESS_CONTROL",
      "/organization-access/",
    ),
    requestRoleAssignment: env(
      "NEXT_PUBLIC_API_ORGANIZATION_ROLE_ASSIGN",
      "/organization-access/roles/assign/",
    ),
    assignDepartmentMember: env(
      "NEXT_PUBLIC_API_DEPARTMENT_MEMBER_ASSIGN",
      "/organization-access/department-members/assign/",
    ),
  },
} as const;
