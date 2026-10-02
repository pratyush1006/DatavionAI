"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import {
  fetchOrganizationCatalog,
  type OrganizationCatalog,
} from "@/lib/backend/onboarding";
import {
  getCities,
  getCountries,
  getCurrentLocation,
  getRegions,
} from "@/lib/backend/geography";
import {
  getSelfServicePlans,
  preflightSelfServiceSignup,
  submitSelfServiceSignup,
  type SelfServicePlan,
  type SignupPreflight,
} from "@/lib/backend/self-service-signup";

type CountryItem = { id: string; name: string };
type RegionItem = { id: string; name: string };
type CityItem = { id: string; name: string; timezone?: string | null };

function countCollection(value: unknown): number {
  if (Array.isArray(value)) return value.length;
  if (value && typeof value === "object") return Object.keys(value as Record<string, unknown>).length;
  return 0;
}

type FormState = {
  category: string;
  organization_type: string;
  size: string;
  plan_id: string;
  plan_code: string;
  organization_name: string;
  display_name: string;
  code: string;
  slug: string;
  organization_email: string;
  support_email: string;
  phone: string;
  website: string;
  first_name: string;
  last_name: string;
  owner_email: string;
  password: string;
  country_ref: string;
  region_ref: string;
  city_ref: string;
  country: string;
  state: string;
  city: string;
  address: string;
  postal_code: string;
  timezone: string;
  registration_number: string;
  tax_number: string;
  license_number: string;
  accreditation: string;
  description: string;
  is_demo: boolean;
};

const INITIAL_FORM: FormState = {
  category: "",
  organization_type: "",
  size: "",
  plan_id: "",
  plan_code: "",
  organization_name: "",
  display_name: "",
  code: "",
  slug: "",
  organization_email: "",
  support_email: "",
  phone: "",
  website: "",
  first_name: "",
  last_name: "",
  owner_email: "",
  password: "",
  country_ref: "",
  region_ref: "",
  city_ref: "",
  country: "",
  state: "",
  city: "",
  address: "",
  postal_code: "",
  timezone: "Asia/Kolkata",
  registration_number: "",
  tax_number: "",
  license_number: "",
  accreditation: "",
  description: "",
  is_demo: false,
};

const STEPS = [
  { id: 1, label: "Organization", description: "What are you building?" },
  { id: 2, label: "Plan", description: "Choose capabilities" },
  { id: 3, label: "Details", description: "Tell us about it" },
  { id: 4, label: "Administrator", description: "Create your owner account" },
  { id: 5, label: "Location", description: "Set your operating region" },
  { id: 6, label: "Review", description: "Confirm and launch" },
] as const;

function humanize(value: string): string {
  return value.replace(/[_-]+/g, " ").replace(/\b\w/g, (match) => match.toUpperCase());
}

function money(plan: SelfServicePlan): string {
  const price = Number(plan.price);
  if (price === 0) return "Free";
  return `${plan.currency} ${price.toLocaleString()}`;
}

function passwordScore(password: string): { label: string; width: string; className: string; percent: number } {
  if (!password) return { label: "", width: "0%", className: "bg-light", percent: 0 };
  if (password.length < 8) return { label: "Too short", width: "35%", className: "bg-danger", percent: 35 };
  if (password.length < 10) return { label: "Good", width: "70%", className: "bg-warning", percent: 70 };
  return { label: "Strong", width: "100%", className: "bg-success", percent: 100 };
}

function Field({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
  required = false,
  help,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
  placeholder?: string;
  required?: boolean;
  help?: string;
}) {
  return (
    <div>
      <label className="form-label small fw-semibold mb-2">
        {label}{required ? <span className="text-danger"> *</span> : null}
      </label>
      <input
        className="form-control form-control-lg border-2 rounded-3 shadow-none"
        aria-label={label}
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={(event) => onChange(event.target.value)}
      />
      {help ? <div className="form-text mt-2">{help}</div> : null}
    </div>
  );
}

function SelectField({
  label,
  value,
  options,
  onChange,
  placeholder,
  disabled = false,
  required = false,
  testId,
}: {
  label: string;
  value: string;
  options: readonly { code: string; name: string }[];
  onChange: (value: string) => void;
  placeholder: string;
  disabled?: boolean;
  required?: boolean;
  testId?: string;
}) {
  return (
    <div>
      <label className="form-label small fw-semibold mb-2">
        {label}{required ? <span className="text-danger"> *</span> : null}
      </label>
      <select
        className="form-select form-select-lg border-2 rounded-3 shadow-none"
        aria-label={label}
        value={value}
        disabled={disabled}
        data-testid={testId}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="">{placeholder}</option>
        {options.map((option) => (
          <option key={option.code} value={option.code}>{option.name}</option>
        ))}
      </select>
    </div>
  );
}

function Progress({ current }: { current: number }) {
  const progress = ((current - 1) / (STEPS.length - 1)) * 100;
  return (
    <div className="mb-5">
      <div className="d-flex justify-content-between small text-secondary mb-2">
        <span>Step {current} of {STEPS.length}</span>
        <span>{STEPS[current - 1].label}</span>
      </div>
      <div className="position-relative" style={{ height: 3 }}>
        <div className="position-absolute top-0 start-0 w-100 rounded-pill bg-secondary-subtle" style={{ height: 3 }} />
        <div className="position-absolute top-0 start-0 rounded-pill bg-primary" style={{ height: 3, width: `${progress}%` }} />
      </div>
      <div className="d-flex justify-content-between mt-3">
        {STEPS.map((step) => {
          const active = step.id === current;
          const done = step.id < current;
          return (
            <div key={step.id} className="text-center flex-fill">
              <div
                className={`mx-auto rounded-circle d-flex align-items-center justify-content-center fw-semibold ${active || done ? "bg-primary text-white" : "bg-light text-secondary"}`}
                style={{ width: 30, height: 30, fontSize: 12 }}
              >
                {done ? "✓" : step.id}
              </div>
              <div className={`small mt-2 d-none d-md-block ${active ? "fw-semibold text-dark" : "text-secondary"}`}>{step.label}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function Heading({ eyebrow, title, description }: { eyebrow: string; title: string; description: string }) {
  return (
    <div className="mb-4">
      <div className="text-primary small fw-bold text-uppercase" style={{ letterSpacing: ".11em" }}>{eyebrow}</div>
      <h2 className="display-6 fw-semibold mt-2 mb-2" style={{ letterSpacing: "-.035em" }}>{title}</h2>
      <p className="text-secondary mb-0" style={{ maxWidth: 690 }}>{description}</p>
    </div>
  );
}

function Summary({
  form,
  selectedPlan,
  typeName,
  sizeName,
}: {
  form: FormState;
  selectedPlan: SelfServicePlan | null;
  typeName: string;
  sizeName: string;
}) {
  const profile = [typeName, sizeName].filter(Boolean).join(" · ");
  const location = [form.city, form.state, form.country].filter(Boolean).join(", ");
  return (
    <aside className="d-flex flex-column gap-3">
      <div className="border-start border-3 border-primary ps-3 py-1">
        <div className="small fw-bold text-uppercase text-primary" style={{ letterSpacing: ".1em" }}>DatavionOS</div>
        <div className="fw-semibold mt-1">One foundation for your organization.</div>
      </div>
      <div className="p-4 bg-light rounded-4">
        <div className="small text-secondary">Your workspace</div>
        <div className="fs-5 fw-semibold mt-1">{form.organization_name || "Organization not named yet"}</div>
        <div className="small text-secondary mt-2">{profile || "Choose your organization profile"}</div>
        <div className="border-top mt-4 pt-3">
          <div className="small text-secondary">Plan</div>
          <div className="fw-semibold mt-1">{selectedPlan?.name || "Not selected"}</div>
          {selectedPlan ? <div className="small text-secondary mt-1">{money(selectedPlan)} · {humanize(selectedPlan.billing_cycle)}</div> : null}
        </div>
        <div className="border-top mt-3 pt-3">
          <div className="small text-secondary">Location</div>
          <div className="fw-semibold mt-1">{location || "Not selected"}</div>
        </div>
      </div>
      <div className="small text-secondary">
        <div className="fw-semibold text-dark mb-2">What happens next</div>
        <div className="d-flex gap-2 mb-2"><span className="text-primary fw-bold">01</span><span>We validate your profile and plan.</span></div>
        <div className="d-flex gap-2 mb-2"><span className="text-primary fw-bold">02</span><span>Your workspace and owner account are provisioned together.</span></div>
        <div className="d-flex gap-2"><span className="text-primary fw-bold">03</span><span>Verify your email, then sign in securely.</span></div>
      </div>
    </aside>
  );
}

function StepRail({ current }: { current: number }) {
  const progress = ((current - 1) / (STEPS.length - 1)) * 100;

  return (
    <div className="mb-5">
      <div className="d-flex align-items-center justify-content-between small text-secondary mb-2">
        <span>Step {current} of {STEPS.length}</span>
        <span>{STEPS[current - 1]?.label ?? "Current"}</span>
      </div>
      <div className="progress" style={{ height: 6 }}>
        <div
          className="progress-bar bg-primary"
          role="progressbar"
          aria-valuenow={Math.max(0, Math.min(100, progress))}
          aria-valuemin={0}
          aria-valuemax={100}
          style={{ width: `${Math.max(0, Math.min(100, progress))}%` }}
        />
      </div>
      <div className="d-flex justify-content-between mt-3 gap-2">
        {STEPS.map((step) => {
          const done = step.id < current;
          const active = step.id === current;

          return (
            <div key={step.id} className="text-center flex-fill">
              <div
                className={`mx-auto rounded-circle d-flex align-items-center justify-content-center fw-semibold ${active || done ? "bg-primary text-white" : "bg-light text-secondary"}`}
                style={{ width: 30, height: 30, fontSize: 12 }}
              >
                {done ? "✓" : step.id}
              </div>
              <div className={`small mt-2 d-none d-md-block ${active ? "fw-semibold text-dark" : "text-secondary"}`}>
                {step.label}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function SectionTitle({
  eyebrow,
  title,
  description,
}: { eyebrow: string; title: string; description: string }) {
  return (
    <div className="mb-4">
      <div className="text-primary small fw-bold text-uppercase" style={{ letterSpacing: ".12em" }}>{eyebrow}</div>
      <h2 className="h3 fw-semibold mt-2 mb-2" style={{ letterSpacing: "-.04em" }}>{title}</h2>
      <p className="text-secondary mb-0" style={{ maxWidth: 700 }}>{description}</p>
    </div>
  );
}

function InputField({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
  required = false,
  help,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
  placeholder?: string;
  required?: boolean;
  help?: string;
}) {
  return <Field label={label} value={value} onChange={onChange} type={type} placeholder={placeholder} required={required} help={help} />;
}

function CheckboxField({
  label,
  checked,
  onChange,
  help,
}: {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  help?: string;
}) {
  return (
    <div className="form-check mt-2">
      <input
        className="form-check-input"
        id="organization-is-demo"
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
      />
      <label className="form-check-label fw-semibold" htmlFor="organization-is-demo">
        {label}
      </label>
      {help ? <div className="form-text">{help}</div> : null}
    </div>
  );
}

function ReviewRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="d-flex justify-content-between align-items-center gap-3 px-4 py-3 border-top">
      <span className="small text-secondary">{label}</span>
      <span className="small fw-semibold text-end">{value || "—"}</span>
    </div>
  );
}

function SidePanel({
  form,
  selectedPlan,
  typeName,
  sizeName,
}: {
  form: FormState;
  selectedPlan: SelfServicePlan | null;
  typeName: string;
  sizeName: string;
}) {
  return <Summary form={form} selectedPlan={selectedPlan} typeName={typeName} sizeName={sizeName} />;
}

export function SelfServiceSignupWizard() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [form, setForm] = useState<FormState>(INITIAL_FORM);
  const [catalog, setCatalog] = useState<OrganizationCatalog | null>(null);
  const [plans, setPlans] = useState<SelfServicePlan[]>([]);
  const [preflight, setPreflight] = useState<SignupPreflight | null>(null);
  const [countries, setCountries] = useState<CountryItem[]>([]);
  const [regions, setRegions] = useState<RegionItem[]>([]);
  const [cities, setCities] = useState<CityItem[]>([]);
  const [loadingCatalog, setLoadingCatalog] = useState(true);
  const [loadingPlans, setLoadingPlans] = useState(false);
  const [loadingCountries, setLoadingCountries] = useState(false);
  const [loadingCurrentLocation, setLoadingCurrentLocation] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [catalogAttempt, setCatalogAttempt] = useState(0);

  useEffect(() => {
    let mounted = true;
    queueMicrotask(() => {
      setLoadingCatalog(true);
    });

    fetchOrganizationCatalog()
      .then((catalogResult) => {
        if (!mounted) return;
        setCatalog(catalogResult);
      })
      .catch((reason) => {
        if (!mounted) return;
        const message = reason instanceof Error ? reason.message : "Unable to load organization options.";
        setError(message);
      })
      .finally(() => mounted && setLoadingCatalog(false));
    return () => { mounted = false; };
  }, [catalogAttempt]);

  useEffect(() => {
    if (step !== 5 || countries.length > 0) return;
    let mounted = true;
    queueMicrotask(() => {
      setLoadingCountries(true);
    });

    getCountries()
      .then((countryResult) => {
        if (!mounted) return;
        setCountries(countryResult);
        setError("");
      })
      .catch((reason) => {
        if (!mounted) return;
        const message = reason instanceof Error ? reason.message : "Unable to load location options.";
        setError(message);
      })
      .finally(() => mounted && setLoadingCountries(false));
    return () => { mounted = false; };
  }, [step, countries.length]);

  const types = useMemo(
    () => (catalog?.types ?? []).filter((item) => !form.category || item.category === form.category),
    [catalog, form.category],
  );
  const selectedPlan = useMemo(() => plans.find((plan) => plan.id === form.plan_id) ?? null, [plans, form.plan_id]);
  const selectedTypeName = useMemo(
    () => types.find((item) => item.code === form.organization_type)?.name ?? humanize(form.organization_type),
    [types, form.organization_type],
  );
  const selectedSizeName = useMemo(
    () => (catalog?.sizes ?? []).find((item) => item.code === form.size)?.name ?? humanize(form.size),
    [catalog, form.size],
  );
  const profileReady = Boolean(form.category && form.organization_type && form.size);
  const password = passwordScore(form.password);

  function update<K extends keyof FormState>(field: K, value: FormState[K]) {
    setForm((current) => ({ ...current, [field]: value }));
    setError("");
  }

  function go(next: number) {
    setError("");
    setStep(next);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function loadPlans() {
    if (!form.category || !form.organization_type || !form.size) {
      setError("Choose your organization category, type and size to continue.");
      return false;
    }
    setLoadingPlans(true);
    setError("");
    try {
      const eligiblePlans = await getSelfServicePlans(form.category, form.organization_type, form.size);
      setPlans(eligiblePlans);
      if (!eligiblePlans.some((plan) => plan.id === form.plan_id)) {
        setForm((current) => ({ ...current, plan_id: "", plan_code: "" }));
      }
      if (!eligiblePlans.length) {
        setError("No eligible plans are currently available for this organization profile.");
        return false;
      }
      go(2);
      return true;
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Unable to load eligible plans.");
      return false;
    } finally {
      setLoadingPlans(false);
    }
  }

  async function validatePlan() {
    if (!selectedPlan) {
      setError("Select a plan to continue.");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const result = await preflightSelfServiceSignup({
        category: form.category,
        organization_type: form.organization_type,
        size: form.size,
        plan_id: selectedPlan.id,
        plan_code: selectedPlan.code,
      });
      setPreflight(result);

      const isPaymentRequiredOnly = result.payment_required_now && !result.eligible;
      if (!result.eligible && !isPaymentRequiredOnly) {
        const message = result.errors.join(" ") || "The selected plan is not eligible for this organization.";
        setError(message);
        return;
      }

      go(3);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Unable to validate the selected plan.");
    } finally {
      setBusy(false);
    }
  }

  function validateOrganization() {
    if (!form.organization_name.trim()) {
      setError("Organization name is required.");
      return;
    }
    if (!form.organization_email.trim()) {
      setError("Primary organization email is required.");
      return;
    }
    go(4);
  }

  function validateOwner() {
    if (!form.first_name.trim() || !form.last_name.trim()) {
      setError("First and last name are required.");
      return;
    }
    if (!form.owner_email.trim()) {
      setError("Administrator email is required.");
      return;
    }
    if (form.password.length < 8) {
      setError("Use a password with at least 8 characters.");
      return;
    }
    go(5);
  }

  function normalizeAddressValue(value: string): string {
    return value.trim().toLowerCase();
  }

  function isUuidLike(value: string): boolean {
    return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value.trim());
  }

  function sanitizeGeographyRefs(value?: string): string | undefined {
    if (!value) return undefined;
    const trimmed = value.trim();
    return isUuidLike(trimmed) ? trimmed : undefined;
  }

  async function loadRegionsForCountry(countryId: string) {
    if (!countryId) {
      setRegions([]);
      return;
    }

    try {
      const items = await getRegions(countryId);
      setRegions(items.map((region) => ({ id: region.id, name: region.name })));
    } catch {
      setRegions([]);
    }
  }

  async function loadCitiesForRegion(regionId: string) {
    if (!regionId) {
      setCities([]);
      return;
    }

    try {
      const items = await getCities(regionId);
      setCities(items.map((city) => ({ id: city.id, name: city.name, timezone: city.timezone })));
    } catch {
      setCities([]);
    }
  }

  async function handleUseCurrentLocation() {
    if (!navigator.geolocation) {
      setError("This browser does not support location detection. Please choose your country manually.");
      return;
    }

    setLoadingCurrentLocation(true);
    setError("");

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const location = await getCurrentLocation(
            position.coords.latitude,
            position.coords.longitude,
            position.coords.accuracy ?? null,
          );

          let nextCountries = countries;
          if (!nextCountries.length) {
            nextCountries = await getCountries();
            setCountries(nextCountries);
          }

          const countryMatch = nextCountries.find((country) => {
            const countryName = normalizeAddressValue(country.name);
            const currentCountry = normalizeAddressValue(location.country);
            return countryName === currentCountry || countryName.includes(currentCountry) || currentCountry.includes(countryName);
          });

          const nextForm: FormState = {
            ...form,
            country: location.country || form.country,
            state: location.state || form.state,
            city: location.city || form.city,
            address: location.formatted_address || form.address,
            postal_code: location.postal_code || form.postal_code,
            timezone: location.timezone || form.timezone || "UTC",
          };

          if (countryMatch) {
            nextForm.country_ref = countryMatch.id;
            nextForm.country = countryMatch.name;
            const nextRegions = await getRegions(countryMatch.id);
            setRegions(nextRegions.map((region) => ({ id: region.id, name: region.name })));

            const regionMatch = nextRegions.find((region) => {
              const regionName = normalizeAddressValue(region.name);
              const currentState = normalizeAddressValue(location.state);
              return regionName === currentState || regionName.includes(currentState) || currentState.includes(regionName);
            });

            if (regionMatch) {
              nextForm.region_ref = regionMatch.id;
              nextForm.state = regionMatch.name;
              const nextCities = await getCities(regionMatch.id);
              setCities(nextCities.map((city) => ({ id: city.id, name: city.name, timezone: city.timezone })));

              const cityMatch = nextCities.find((city) => {
                const cityName = normalizeAddressValue(city.name);
                const currentCity = normalizeAddressValue(location.city);
                return cityName === currentCity || cityName.includes(currentCity) || currentCity.includes(cityName);
              });

              if (cityMatch) {
                nextForm.city_ref = cityMatch.id;
                nextForm.city = cityMatch.name;
                nextForm.timezone = cityMatch.timezone || nextForm.timezone;
              } else {
                nextForm.city = location.city || nextForm.city;
              }
            }
          }

          if (!nextForm.country) {
            nextForm.country = location.country || form.country;
          }
          if (!nextForm.state) {
            nextForm.state = location.state || form.state;
          }
          if (!nextForm.city) {
            nextForm.city = location.city || form.city;
          }
          if (!nextForm.address && location.formatted_address) {
            nextForm.address = location.formatted_address;
          }
          if (!nextForm.postal_code && location.postal_code) {
            nextForm.postal_code = location.postal_code;
          }

          setForm(nextForm);
          setError("");
        } catch (reason) {
          const message = reason instanceof Error ? reason.message : "Unable to determine your current location.";
          setError(message);
        } finally {
          setLoadingCurrentLocation(false);
        }
      },
      (geoError) => {
        setError(
          geoError.code === 1
            ? "Location access was denied. Please choose your location manually."
            : "We could not read your device location. Please choose a location manually.",
        );
        setLoadingCurrentLocation(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 60000,
      },
    );
  }

  function validateLocation() {
    if (!form.country_ref && !form.country.trim()) {
      setError("Choose your country to continue.");
      return;
    }
    go(6);
  }

  async function submit() {
    if (!selectedPlan || !preflight?.eligible) {
      setError("Your plan eligibility needs to be validated before signup.");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const countryRef = sanitizeGeographyRefs(form.country_ref);
      const regionRef = sanitizeGeographyRefs(form.region_ref);
      const cityRef = sanitizeGeographyRefs(form.city_ref);

      const result = await submitSelfServiceSignup({
        account: {
          email: form.owner_email.trim().toLowerCase(),
          password: form.password,
          first_name: form.first_name.trim(),
          last_name: form.last_name.trim(),
          phone: form.phone.trim() || undefined,
        },
        organization: {
          name: form.organization_name.trim(),
          display_name: form.display_name.trim() || undefined,
          code: form.code.trim().toUpperCase() || undefined,
          slug: form.slug.trim().toLowerCase() || undefined,
          category: form.category,
          organization_type: form.organization_type,
          size: form.size,
          email: form.organization_email.trim().toLowerCase(),
          support_email: form.support_email.trim().toLowerCase() || undefined,
          phone: form.phone.trim() || undefined,
          website: form.website.trim() || undefined,
          address: form.address.trim() || undefined,
          city: form.city.trim() || undefined,
          state: form.state.trim() || undefined,
          country: form.country.trim() || undefined,
          country_ref: countryRef,
          region_ref: regionRef,
          city_ref: cityRef,
          postal_code: form.postal_code.trim() || undefined,
          timezone: form.timezone.trim() || undefined,
          registration_number: form.registration_number.trim() || undefined,
          tax_number: form.tax_number.trim() || undefined,
          license_number: form.license_number.trim() || undefined,
          accreditation: form.accreditation.trim() || undefined,
          description: form.description.trim() || undefined,
          is_demo: false,
          plan_id: selectedPlan.id,
          plan_code: selectedPlan.code,
        },
      });

      if (result.payment.required_now) {
        setError("This plan requires payment before the workspace can be created.");
        return;
      }

      sessionStorage.setItem("datavionos.signup.email", result.account.email);
      router.replace(`/verify-email?email=${encodeURIComponent(result.account.email)}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Organization registration failed.");
    } finally {
      setBusy(false);
    }
  }



  return (
    <main className="min-vh-100 bg-white text-dark">
      <nav className="border-bottom bg-white">
        <div className="container py-3 d-flex align-items-center justify-content-between gap-3">
          <Link href="/" className="text-decoration-none text-dark fw-bold" style={{ letterSpacing: ".09em" }}>DATAVIONAI</Link>
          <div className="small text-secondary">
            Already have an account? <Link href="/login" className="fw-semibold text-primary text-decoration-none">Sign in</Link>
          </div>
        </div>
      </nav>

      <div className="container py-5 py-lg-6">
        <div className="mx-auto" style={{ maxWidth: 1180 }}>
          <header className="mb-5">
            <div className="small text-primary fw-bold text-uppercase mb-3" style={{ letterSpacing: ".13em" }}>Create your organization</div>
            <div className="row align-items-end g-4">
              <div className="col-lg-9">
                <h1 className="display-4 fw-semibold mb-3" style={{ letterSpacing: "-.055em", lineHeight: 1.02 }}>Build the healthcare workspace your organization can grow on.</h1>
                <p className="lead text-secondary mb-0" style={{ maxWidth: 820, fontSize: "1.08rem" }}>
                  Start with your organization profile. DatavionOS uses it to shape the eligible plan, workspace and capabilities available to your teams. You do not need an existing DatavionOS account to begin.
                </p>
              </div>
              <div className="col-lg-3">
                <div className="small text-secondary text-lg-end">One foundation.<br />Focused experiences.<br />Flexible growth.</div>
              </div>
            </div>
          </header>

          <StepRail current={step} />

          {error ? (
            <div className="border rounded-3 px-3 py-3 mb-4 bg-light d-flex align-items-start justify-content-between gap-3" role="alert">
              <div>
                <div className="fw-semibold text-dark">We could not continue</div>
                <div className="small text-secondary mt-1">{error}</div>
              </div>
              {loadingCatalog === false && !catalog ? (
                <button className="btn btn-sm btn-outline-primary" type="button" onClick={() => setCatalogAttempt((value) => value + 1)}>Retry</button>
              ) : null}
            </div>
          ) : null}

          <div className="row g-5">
            <div className="col-lg-8">
              <div className="border rounded-4 bg-white p-4 p-lg-5">
                {step === 1 ? (
                  <section>
                    <SectionTitle eyebrow="01 · Organization" title="Start with your organization." description="These choices define the profile that DatavionOS can offer. Eligibility remains controlled by the backend." />
                    {loadingCatalog ? (
                      <div className="py-5 text-center text-secondary"><div className="spinner-border spinner-border-sm me-2" />Loading organization options…</div>
                    ) : !catalog ? (
                      <div className="py-5 text-center">
                        <div className="small text-primary fw-bold text-uppercase mb-2" style={{ letterSpacing: ".1em" }}>DatavionOS</div>
                        <div className="h5 fw-semibold">Organization options are temporarily unavailable.</div>
                        <div className="small text-secondary mt-2">The registration page is public; retry to reconnect to the onboarding catalog.</div>
                        <button className="btn btn-primary mt-4 rounded-3 px-4" type="button" onClick={() => setCatalogAttempt((value) => value + 1)}>Retry</button>
                      </div>
                    ) : (
                      <>
                        <div className="row g-4">
                          <div className="col-12">
                            <SelectField label="Organization category" value={form.category} options={catalog.categories as readonly { code: string; name: string }[]} onChange={(value) => { setForm((current) => ({ ...current, category: value, organization_type: "", size: "", plan_id: "", plan_code: "" })); setPlans([]); setPreflight(null); setError(""); }} placeholder="Choose a category" required testId="organization-category" />
                          </div>
                          <div className="col-md-6">
                            <SelectField label="Organization type" value={form.organization_type} options={types as readonly { code: string; name: string }[]} onChange={(value) => { setForm((current) => ({ ...current, organization_type: value, plan_id: "", plan_code: "" })); setPlans([]); setPreflight(null); }} placeholder={form.category ? "Choose an organization type" : "Choose a category first"} disabled={!form.category} required testId="organization-type" />
                          </div>
                          <div className="col-md-6">
                            <SelectField label="Organization size" value={form.size} options={(catalog.sizes ?? []) as readonly { code: string; name: string }[]} onChange={(value) => update("size", value)} placeholder="Choose a size" required testId="organization-size" />
                          </div>
                        </div>

                        <div className="border-top mt-5 pt-4 d-flex flex-column flex-sm-row align-items-sm-center justify-content-between gap-3">
                          <div className="small text-secondary">Your profile determines which plans can be offered next.</div>
                          <button className="btn btn-primary btn-lg rounded-3 px-4" type="button" disabled={!profileReady || loadingPlans} onClick={() => void loadPlans()}>
                            {loadingPlans ? "Finding plans…" : "Continue →"}
                          </button>
                        </div>
                      </>
                    )}
                  </section>
                ) : null}

                {step === 2 ? (
                  <section>
                    <SectionTitle eyebrow="02 · Plan" title="Choose how your workspace should start." description={`Plans returned by DatavionOS for ${selectedTypeName || humanize(form.organization_type)} · ${selectedSizeName || humanize(form.size)}.`} />

                    <div className="mb-4">
                      <label className="form-label small fw-semibold mb-2">Available plans</label>
                      <select
                        className="form-select form-select-lg border-2 rounded-3 shadow-none"
                        aria-label="Select plan"
                        value={form.plan_id}
                        onChange={(event) => {
                          const plan = plans.find((item) => item.id === event.target.value) ?? null;
                          update("plan_id", plan?.id ?? "");
                          update("plan_code", plan?.code ?? "");
                          setPreflight(null);
                        }}
                      >
                        <option value="">Select a plan</option>
                        {plans.map((plan) => (
                          <option key={plan.id} value={plan.id}>
                            {plan.name} — {money(plan)} / {humanize(plan.billing_cycle)}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="border rounded-4 bg-light p-3 p-lg-4" style={{ minHeight: 0 }}>
                      {selectedPlan ? (
                        <>
                          <div className="d-flex align-items-center justify-content-between gap-2 flex-wrap mb-2">
                            <div>
                              <div className="small text-primary fw-bold text-uppercase" style={{ letterSpacing: ".1em" }}>Selected plan</div>
                              <div className="h4 fw-semibold mt-1 mb-0">{selectedPlan.name}</div>
                            </div>
                            {selectedPlan.is_featured ? (
                              <span className="badge rounded-pill text-bg-primary px-2 py-1">Featured</span>
                            ) : null}
                          </div>

                          <div className="display-6 fw-semibold mb-1" style={{ fontSize: "2rem", letterSpacing: "-.04em", lineHeight: 1.1 }}>{money(selectedPlan)}</div>
                          <div className="small text-secondary mb-2">{humanize(selectedPlan.billing_cycle)}</div>

                          <p className="text-secondary mb-3" style={{ fontSize: "0.95rem" }}>{selectedPlan.description || "A DatavionOS workspace plan configured for your organization profile."}</p>

                          <div className="d-flex flex-wrap gap-2 gap-md-3 small text-secondary">
                            <span>{countCollection(selectedPlan.modules)} modules</span>
                            <span>•</span>
                            <span>{countCollection(selectedPlan.features)} capabilities</span>
                            {Number(selectedPlan.price) > 0 ? <><span>•</span><span className="text-warning-emphasis fw-semibold">Payment required before setup</span></> : null}
                            {selectedPlan.trial_days > 0 ? <><span>•</span><span className="text-primary fw-semibold">{selectedPlan.trial_days}-day trial{Number(selectedPlan.price) > 0 ? " after payment" : ""}</span></> : null}
                          </div>
                        </>
                      ) : (
                        <div className="text-secondary">Choose a plan from the dropdown to continue.</div>
                      )}
                    </div>

                    <div className="border-top mt-5 pt-4 d-flex justify-content-between gap-3">
                      <button className="btn btn-outline-secondary rounded-3 px-4" type="button" onClick={() => go(1)}>← Back</button>
                      <button className="btn btn-primary btn-lg rounded-3 px-4" type="button" disabled={!selectedPlan || busy} onClick={() => void validatePlan()}>{busy ? "Checking…" : "Continue →"}</button>
                    </div>
                  </section>
                ) : null}

                {step === 3 ? (
                  <section>
                    <SectionTitle eyebrow="03 · Details" title="Tell us about the organization itself." description="These details become part of the organization workspace and can be completed further after setup." />
                    <div className="row g-4">
                      <div className="col-12"><InputField label="Organization name" value={form.organization_name} onChange={(value) => update("organization_name", value)} placeholder="e.g. Sunrise Multispeciality Clinic" required /></div>
                      <div className="col-md-6"><InputField label="Display name" value={form.display_name} onChange={(value) => update("display_name", value)} placeholder="e.g. Sunrise Clinic" /></div>
                      <div className="col-md-3"><InputField label="Organization code" value={form.code} onChange={(value) => update("code", value)} placeholder="SUNRISE" help="Optional; generated from the name when omitted." /></div>
                      <div className="col-md-3"><InputField label="URL slug" value={form.slug} onChange={(value) => update("slug", value)} placeholder="sunrise-clinic" help="Optional; generated from the name when omitted." /></div>
                      <div className="col-md-6"><InputField label="Primary organization email" value={form.organization_email} onChange={(value) => update("organization_email", value)} type="email" placeholder="hello@yourorganization.com" required /></div>
                      <div className="col-md-6"><InputField label="Support email" value={form.support_email} onChange={(value) => update("support_email", value)} type="email" placeholder="support@yourorganization.com" /></div>
                      <div className="col-md-6"><InputField label="Phone" value={form.phone} onChange={(value) => update("phone", value)} placeholder="+91…" /></div>
                      <div className="col-md-6"><InputField label="Website" value={form.website} onChange={(value) => update("website", value)} placeholder="https://…" /></div>
                      <div className="col-12"><InputField label="Description" value={form.description} onChange={(value) => update("description", value)} placeholder="A short description of your organization" /></div>
                      <div className="col-md-4"><InputField label="Registration number" value={form.registration_number} onChange={(value) => update("registration_number", value)} /></div>
                      <div className="col-md-4"><InputField label="License number" value={form.license_number} onChange={(value) => update("license_number", value)} /></div>
                      <div className="col-md-4"><InputField label="Tax number" value={form.tax_number} onChange={(value) => update("tax_number", value)} /></div>
                      <div className="col-md-6"><InputField label="Accreditation" value={form.accreditation} onChange={(value) => update("accreditation", value)} placeholder="e.g. NABH" /></div>
                    </div>
                    <div className="border-top mt-5 pt-4 d-flex justify-content-between gap-3"><button className="btn btn-outline-secondary rounded-3 px-4" type="button" onClick={() => go(2)}>← Back</button><button className="btn btn-primary btn-lg rounded-3 px-4" type="button" onClick={validateOrganization}>Continue →</button></div>
                  </section>
                ) : null}

                {step === 4 ? (
                  <section>
                    <SectionTitle eyebrow="04 · Administrator" title="Create the person who will own this workspace." description="The administrator becomes the first organization owner. Verification and login OTPs are sent to this email after signup." />
                    <div className="row g-4">
                      <div className="col-md-6"><InputField label="First name" value={form.first_name} onChange={(value) => update("first_name", value)} placeholder="First name" required /></div>
                      <div className="col-md-6"><InputField label="Last name" value={form.last_name} onChange={(value) => update("last_name", value)} placeholder="Last name" required /></div>
                      <div className="col-12"><InputField label="Administrator email" value={form.owner_email} onChange={(value) => update("owner_email", value)} type="email" placeholder="you@yourorganization.com" help="This becomes the owner's login email." required /></div>
                      <div className="col-12"><InputField label="Password" value={form.password} onChange={(value) => update("password", value)} type="password" placeholder="Create a strong password" help="Use at least 8 characters." required />{form.password ? <><div className="progress mt-3" style={{ height: 4 }}><div className="progress-bar bg-primary" style={{ width: `${password.percent}%` }} /></div><div className="small text-secondary mt-2">{password.label}</div></> : null}</div>
                    </div>
                    <div className="border rounded-3 p-3 mt-4 bg-light small text-secondary">You can add more users, departments, teams and roles after the workspace is created.</div>
                    <div className="border-top mt-5 pt-4 d-flex justify-content-between gap-3"><button className="btn btn-outline-secondary rounded-3 px-4" type="button" onClick={() => go(3)}>← Back</button><button className="btn btn-primary btn-lg rounded-3 px-4" type="button" onClick={validateOwner}>Continue →</button></div>
                  </section>
                ) : null}

                {step === 5 ? (
                  <section>
                    <SectionTitle eyebrow="05 · Location" title="Set the operating context for your organization." description="Country, region and city are loaded from DatavionOS geography master data." />

                    <div className="d-flex justify-content-between align-items-center gap-3 mb-4">
                      <div className="small text-secondary">Use your current device location or select a region manually.</div>
                      <button
                        className="btn btn-outline-primary btn-sm rounded-3"
                        type="button"
                        onClick={() => void handleUseCurrentLocation()}
                        disabled={loadingCurrentLocation}
                      >
                        {loadingCurrentLocation ? "Detecting…" : "Use current location"}
                      </button>
                    </div>

                    {loadingCountries ? (
                      <div className="py-5 text-center text-secondary">
                        <div className="spinner-border spinner-border-sm me-2" />
                        Loading countries…
                      </div>
                    ) : (
                      <div className="row g-4">
                        <div className="col-md-4">
                          <SelectField
                            label="Country"
                            value={form.country_ref}
                            options={countries.map((item) => ({ code: item.id, name: item.name }))}
                            onChange={(value) => {
                              const item = countries.find((country) => country.id === value);
                              setForm((current) => ({
                                ...current,
                                country_ref: value,
                                country: item?.name ?? current.country,
                                region_ref: "",
                                state: "",
                                city_ref: "",
                                city: "",
                              }));
                              setRegions([]);
                              setCities([]);
                              if (value) {
                                void loadRegionsForCountry(value);
                              }
                            }}
                            placeholder="Choose country"
                            required
                          />
                        </div>

                        <div className="col-md-4">
                          <SelectField
                            label="State / region"
                            value={form.region_ref}
                            options={regions.map((item) => ({ code: item.id, name: item.name }))}
                            onChange={(value) => {
                              const item = regions.find((region) => region.id === value);
                              setForm((current) => ({
                                ...current,
                                region_ref: value,
                                state: item?.name ?? current.state,
                                city_ref: "",
                                city: "",
                              }));
                              setCities([]);
                              if (value) {
                                void loadCitiesForRegion(value);
                              }
                            }}
                            placeholder={form.country_ref ? "Choose region" : "Choose country first"}
                            disabled={!form.country_ref}
                          />
                        </div>

                        <div className="col-md-4">
                          <SelectField
                            label="City"
                            value={form.city_ref}
                            options={cities.map((item) => ({ code: item.id, name: item.name }))}
                            onChange={(value) => {
                              const item = cities.find((city) => city.id === value);
                              setForm((current) => ({
                                ...current,
                                city_ref: value,
                                city: item?.name ?? current.city,
                                timezone: item?.timezone ?? current.timezone,
                              }));
                            }}
                            placeholder={form.region_ref ? "Choose city" : "Choose region first"}
                            disabled={!form.region_ref}
                          />
                        </div>

                        <div className="col-md-8">
                          <InputField
                            label="Street address"
                            value={form.address}
                            onChange={(value) => update("address", value)}
                            placeholder="Building, street, locality"
                          />
                        </div>

                        <div className="col-md-4">
                          <InputField
                            label="Postal code"
                            value={form.postal_code}
                            onChange={(value) => update("postal_code", value)}
                            placeholder="Postal code"
                          />
                        </div>

                        <div className="col-12">
                          <InputField
                            label="Timezone"
                            value={form.timezone}
                            onChange={(value) => update("timezone", value)}
                            placeholder="Asia/Kolkata"
                          />
                        </div>
                      </div>
                    )}

                    <div className="border-top mt-5 pt-4 d-flex justify-content-between gap-3">
                      <button className="btn btn-outline-secondary rounded-3 px-4" type="button" onClick={() => go(4)}>← Back</button>
                      <button className="btn btn-primary btn-lg rounded-3 px-4" type="button" onClick={validateLocation}>Review workspace →</button>
                    </div>
                  </section>
                ) : null}

                {step === 6 ? (
                  <section>
                    <SectionTitle eyebrow="06 · Review" title="Review your workspace before you launch it." description="The backend performs the final validation and provisions the owner account, organization and subscription." />
                    <div className="border rounded-4 overflow-hidden bg-white">
                      <div className="px-4 py-3 bg-light small fw-semibold">Organization</div>
                      <ReviewRow label="Name" value={form.organization_name} /><ReviewRow label="Profile" value={[selectedTypeName, selectedSizeName].filter(Boolean).join(" · ")} /><ReviewRow label="Email" value={form.organization_email} />
                      <div className="px-4 py-3 bg-light small fw-semibold">Plan</div><ReviewRow label="Selected plan" value={selectedPlan?.name ?? ""} /><ReviewRow label="Billing" value={selectedPlan ? `${money(selectedPlan)} · ${humanize(selectedPlan.billing_cycle)}` : ""} />
                      <div className="px-4 py-3 bg-light small fw-semibold">Workspace administrator</div><ReviewRow label="Name" value={[form.first_name, form.last_name].filter(Boolean).join(" ")} /><ReviewRow label="Email" value={form.owner_email} />
                      <div className="px-4 py-3 bg-light small fw-semibold">Location</div><ReviewRow label="Location" value={[form.city, form.state, form.country].filter(Boolean).join(", ")} /><ReviewRow label="Timezone" value={form.timezone} />
                    </div>
                    {preflight?.payment_required_now ? (
                      <div className="alert alert-warning border-0 rounded-3 mt-4 d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3">
                        <div>
                          <div className="fw-semibold">This plan requires payment before the workspace can be created.</div>
                          <div className="small mt-1">Complete billing before continuing to setup.</div>
                        </div>
                        <button
                          className="btn btn-warning text-dark fw-semibold rounded-3"
                          type="button"
                          onClick={() => {
                            if (!selectedPlan) return;
                            const params = new URLSearchParams({
                              plan: selectedPlan.name,
                              amount: selectedPlan.price,
                              currency: selectedPlan.currency,
                              cycle: selectedPlan.billing_cycle,
                            });
                            router.push(`/billing?${params.toString()}`);
                          }}
                        >
                          Pay now
                        </button>
                      </div>
                    ) : null}
                    <div className="mt-4 p-4 rounded-4 border"><div className="fw-semibold">Ready to create your workspace?</div><div className="small text-secondary mt-1">After signup, we will send a verification code to the administrator email.</div></div>
                    <div className="border-top mt-5 pt-4 d-flex justify-content-between gap-3"><button className="btn btn-outline-secondary rounded-3 px-4" type="button" onClick={() => go(5)} disabled={busy}>← Back</button><button className="btn btn-primary btn-lg rounded-3 px-4" type="button" onClick={() => void submit()} disabled={busy || !selectedPlan || !preflight?.eligible || Boolean(preflight?.payment_required_now)}>{busy ? "Creating workspace…" : preflight?.payment_required_now ? "Payment required" : "Create workspace →"}</button></div>
                  </section>
                ) : null}
              </div>
            </div>

            <div className="col-lg-4">
              <SidePanel form={form} selectedPlan={selectedPlan} typeName={selectedTypeName} sizeName={selectedSizeName} />
            </div>
          </div>

          <footer className="mt-5 pt-4 border-top d-flex flex-column flex-md-row justify-content-between gap-2 small text-secondary">
            <span>DatavionOS — The AI Operating System for Healthcare</span>
            <span>Secure self-service onboarding · No existing account required</span>
          </footer>
        </div>
      </div>
    </main>
  );
}

export default SelfServiceSignupWizard;
