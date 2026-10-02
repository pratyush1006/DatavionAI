import OrganizationRegistrationForm from "@/components/forms/OrganizationRegistrationForm";

/**
 * Keep the legacy /register entry point on the canonical public
 * organization-signup workflow. The workflow owns catalog loading,
 * preflight validation, and submission to /onboarding/signup/.
 */
export default function RegisterPage() {
  return <OrganizationRegistrationForm />;
}
