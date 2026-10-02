"use client";

import { useEffect, useState } from "react";

import {
  getCities,
  getCountries,
  getOrganizationCatalog,
  getStates,
  resolveCurrentLocation,
  type CatalogOption,
  type GeographyOption,
} from "@/core/api/organization-registration";
import {
  getSelfServicePlans,
  type SelfServicePlan,
} from "@/lib/backend/self-service-signup";

type Props = {
  values: {
    organizationName: string;
    organizationType: string;
    organizationCategory: string;
    organizationSize: string;
    subscriptionPlan: string;
    subscriptionPlanCode: string;
    adminEmail: string;
    country: string;
    state: string;
    city: string;
    timezone: string;
    countryId: string;
    stateId: string;
    cityId: string;
    addressLine1: string;
    addressLine2: string;
    postalCode: string;
    latitude?: number;
    longitude?: number;
  };
  onChange: (
    field: string,
    value: string | number,
  ) => void;
};

export default function OrganizationRegistrationBusinessDetails({
  values,
  onChange,
}: Props) {
  const [types, setTypes] = useState<CatalogOption[]>([]);
  const [categories, setCategories] = useState<CatalogOption[]>([]);
  const [sizes, setSizes] = useState<CatalogOption[]>([]);
  const [planResult, setPlanResult] = useState<{
    key: string;
    plans: SelfServicePlan[];
  }>({ key: "", plans: [] });

  const [countries, setCountries] = useState<GeographyOption[]>([]);
  const [states, setStates] = useState<GeographyOption[]>([]);
  const [cities, setCities] = useState<GeographyOption[]>([]);

  const [loading, setLoading] = useState(true);
  const [locationLoading, setLocationLoading] = useState(false);
  const [locationDetected, setLocationDetected] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    Promise.all([
      getOrganizationCatalog(),
      getCountries(),
    ])
      .then(([catalog, countryData]) => {
          if (!active) {
            return;
          }

          setTypes(catalog.types);
          setCategories(catalog.categories);
          setSizes(catalog.sizes);
          setCountries(countryData);
        })
      .catch((reason: unknown) => {
        if (!active) {
          return;
        }

        setError(
          reason instanceof Error
            ? reason.message
            : "Unable to load registration catalogs.",
        );
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;

    if (
      !values.organizationCategory ||
      !values.organizationType ||
      !values.organizationSize
    ) {
      return () => {
        active = false;
      };
    }

    const key = [
      values.organizationCategory,
      values.organizationType,
      values.organizationSize,
    ].join(":");

    getSelfServicePlans(
      values.organizationCategory,
      values.organizationType,
      values.organizationSize,
    )
      .then((items) => {
        if (active) {
          setPlanResult({ key, plans: items });
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(
            reason instanceof Error
              ? reason.message
              : "Unable to load eligible subscription plans.",
          );
        }
      });

    return () => {
      active = false;
    };
  }, [
    values.organizationCategory,
    values.organizationType,
    values.organizationSize,
  ]);

  const profileKey = [
    values.organizationCategory,
    values.organizationType,
    values.organizationSize,
  ].join(":");
  const plans = planResult.key === profileKey ? planResult.plans : [];

  useEffect(() => {
    if (!values.countryId) {
      return;
    }

    let active = true;

    getStates(values.countryId)
      .then((items) => {
        if (active) {
          setStates(items);
        }
      })
      .catch(() => {
        if (active) {
          setStates([]);
        }
      });

    return () => {
      active = false;
    };
  }, [values.countryId]);

  useEffect(() => {
    if (!values.stateId) {
      return;
    }

    let active = true;

    getCities(values.stateId)
      .then((items) => {
        if (active) {
          setCities(items);
        }
      })
      .catch(() => {
        if (active) {
          setCities([]);
        }
      });

    return () => {
      active = false;
    };
  }, [values.stateId]);

  function detectCurrentLocation() {
    if (!navigator.geolocation) {
      setError("Browser geolocation is not available.");
      return;
    }

    setLocationLoading(true);
    setError("");

    navigator.geolocation.getCurrentPosition(
      (position) => {
        void resolveCurrentLocation(
          position.coords.latitude,
          position.coords.longitude,
          position.coords.accuracy,
        )
          .then((location) => {
            onChange("latitude", location.latitude);
            onChange("longitude", location.longitude);
            onChange("addressLine1", location.formatted_address);
            onChange("country", location.country);
            onChange("state", location.state);
            onChange("city", location.city);
            onChange("postalCode", location.postal_code);
            const reference = location.reference;
            if (typeof reference.country_id === "string") {
              onChange("countryId", reference.country_id);
            }
            if (typeof reference.region_id === "string") {
              onChange("stateId", reference.region_id);
            }
            if (typeof reference.city_id === "string") {
              onChange("cityId", reference.city_id);
            }
            setLocationDetected(true);
          })
          .catch((reason: unknown) => {
            setError(
              reason instanceof Error
                ? reason.message
                : "Unable to resolve the current location.",
            );
            setLocationDetected(false);
          })
          .finally(() => setLocationLoading(false));
      },
      () => {
        setError(
          "Unable to detect your current location. Please select the address manually.",
        );
        setLocationDetected(false);
        setLocationLoading(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000,
      },
    );
  }

  /*
   * Do not synchronously clear dependent state from effects.
   *
   * When the parent geography changes, the selected child value is
   * cleared by the corresponding user interaction below. The effect
   * only synchronizes asynchronously with the backend.
   *
   * For rendering, an empty parent means there is no valid child
   * catalog to display.
   */
  const visibleStates = values.countryId
    ? states
    : [];

  const visibleCities = values.stateId
    ? cities
    : [];

  if (loading) {
    return (
      <div className="alert alert-info">
        Loading organization and geography configuration...
      </div>
    );
  }

  return (
    <section
      className="card border-0 shadow-sm mb-4"
      data-testid="organization-business-details"
    >
      <div className="card-body p-4">
        <div className="mb-4">
          <h2 className="h5 mb-1">
            Organization &amp; Business Details
          </h2>

          <p className="text-muted mb-0">
            These values are controlled by DatavionOS backend catalogs.
          </p>
        </div>

        {error && (
          <div
            className="alert alert-danger"
            role="alert"
          >
            {error}
          </div>
        )}

        <div className="row g-3">
          <div className="col-md-6">
            <label className="form-label">
              Organization Type
            </label>

            <select
              className="form-select"
              data-testid="organization-type"
              value={values.organizationType}
              onChange={(event) => {
                onChange(
                  "organizationType",
                  event.target.value,
                );
                onChange("organizationSize", "");
                onChange("subscriptionPlan", "");
                onChange("subscriptionPlanCode", "");
              }}
              required
            >
              <option value="">
                Select type
              </option>

              {types
                .filter((item) => !item.category || item.category === values.organizationCategory)
                .map((item) => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name}
                </option>
                ))}
            </select>
          </div>

          <div className="col-md-6">
            <label className="form-label">
              Organization Category
            </label>

            <select
              className="form-select"
              data-testid="organization-category"
              value={values.organizationCategory}
              onChange={(event) => {
                onChange(
                  "organizationCategory",
                  event.target.value,
                );
                onChange("organizationType", "");
                onChange("organizationSize", "");
                onChange("subscriptionPlan", "");
                onChange("subscriptionPlanCode", "");
              }}
              required
            >
              <option value="">
                Select category
              </option>

              {categories.map((item) => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name}
                </option>
              ))}
            </select>
          </div>

          <div className="col-md-6">
            <label className="form-label">
              Organization Size
            </label>

            <select
              className="form-select"
              data-testid="organization-size"
              value={values.organizationSize}
              onChange={(event) => {
                onChange(
                  "organizationSize",
                  event.target.value,
                );
                onChange("subscriptionPlan", "");
                onChange("subscriptionPlanCode", "");
              }}
              required
            >
              <option value="">
                Select size
              </option>

              {sizes.map((item) => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name}
                </option>
              ))}
            </select>
          </div>

          <div className="col-12">
            <label className="form-label">
              Subscription Plan
            </label>

            <div className="row g-3">
              {plans.map((plan) => (
                <div
                  className="col-md-4"
                  key={plan.id}
                >
                  <button
                    type="button"
                    className={
                      values.subscriptionPlan === plan.id
                        ? "card w-100 text-start border-primary shadow-sm"
                        : "card w-100 text-start border"
                    }
                    data-testid={`subscription-plan-${plan.id}`}
                    onClick={() =>
                      {
                        onChange("subscriptionPlan", plan.id);
                        onChange("subscriptionPlanCode", plan.code);
                      }
                    }
                    aria-pressed={values.subscriptionPlan === plan.id}
                  >
                    <div className="card-body">
                      <div className="fw-semibold">
                        {plan.name}
                      </div>

                      {plan.description && (
                        <div className="small text-muted mt-1">
                          {plan.description}
                        </div>
                      )}

                      {plan.price !== undefined && (
                        <div className="mt-2">
                          <strong>
                            {plan.currency ?? ""} {Number(plan.price).toLocaleString()}
                          </strong>

                          {plan.billing_cycle && (
                            <span className="text-muted">
                              {" "}/ {plan.billing_cycle}
                            </span>
                          )}
                        </div>
                      )}

                      <div className="small text-body-secondary mt-2">
                        {plan.trial_days} day trial
                      </div>

                      {Array.isArray(plan.modules) && plan.modules.length > 0 ? (
                        <ul className="small text-body-secondary mt-3 mb-0 ps-3">
                          {plan.modules.slice(0, 5).map((module) => (
                            <li key={String(module)}>{String(module).replace(/[_-]+/g, " ")}</li>
                          ))}
                        </ul>
                      ) : null}
                    </div>
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="col-12">
            <hr />

            <h3 className="h6">
              Organization Address
            </h3>
          </div>

          <div className="col-md-6">
            <label className="form-label">
              Country
            </label>

            <select
              className="form-select"
              data-testid="organization-country"
              value={values.countryId}
              onChange={(event) => {
                const selected = countries.find((item) => item.id === event.target.value);
                onChange("countryId", event.target.value);
                onChange("country", selected?.name ?? "");
                onChange("stateId", "");
                onChange("state", "");
                onChange("cityId", "");
                onChange("city", "");
                onChange("timezone", "");
              }}
              required
            >
              <option value="">
                Select country
              </option>

              {countries.map((item) => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name}
                </option>
              ))}
            </select>
          </div>

          <div className="col-md-6">
            <label className="form-label">
              State
            </label>

            <select
              className="form-select"
              data-testid="organization-state"
              value={values.stateId}
              disabled={!values.countryId}
              onChange={(event) => {
                const selected = states.find((item) => item.id === event.target.value);
                onChange("stateId", event.target.value);
                onChange("state", selected?.name ?? "");
                onChange("cityId", "");
                onChange("city", "");
                onChange("timezone", "");
              }}
              required
            >
              <option value="">
                Select state
              </option>

              {visibleStates.map((item) => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name}
                </option>
              ))}
            </select>
          </div>

          <div className="col-md-6">
            <label className="form-label">
              City
            </label>

            <select
              className="form-select"
              data-testid="organization-city"
              value={values.cityId}
              disabled={!values.stateId}
              onChange={(event) => {
                const selected = cities.find((item) => item.id === event.target.value);
                onChange("cityId", event.target.value);
                onChange("city", selected?.name ?? "");
                onChange("timezone", selected?.timezone ?? "");
              }}
              required
            >
              <option value="">
                Select city
              </option>

              {visibleCities.map((item) => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name}
                </option>
              ))}
            </select>
          </div>

          <div className="col-12">
            <button
              type="button"
              className="btn btn-outline-secondary"
              data-testid="organization-detect-location"
              onClick={detectCurrentLocation}
              disabled={locationLoading}
            >
              {locationLoading
                ? "Detecting location..."
                : "Use Current Location"}
            </button>

            {locationDetected && (
              <span
                className="small text-muted ms-3"
                data-testid="organization-location-status"
                role="status"
              >
                Location detected
              </span>
            )}
          </div>

          <div className="col-md-8">
            <label className="form-label">
              Address Line 1
            </label>

            <input
              className="form-control"
              data-testid="organization-address-line1"
              value={values.addressLine1}
              onChange={(event) =>
                onChange(
                  "addressLine1",
                  event.target.value,
                )
              }
              required
            />
          </div>

          <div className="col-md-4">
            <label className="form-label">
              Postal Code
            </label>

            <input
              className="form-control"
              data-testid="organization-postal-code"
              value={values.postalCode}
              onChange={(event) =>
                onChange(
                  "postalCode",
                  event.target.value,
                )
              }
              required
            />
          </div>

          <div className="col-12">
            <label className="form-label">
              Address Line 2
            </label>

            <input
              className="form-control"
              data-testid="organization-address-line2"
              value={values.addressLine2}
              onChange={(event) =>
                onChange(
                  "addressLine2",
                  event.target.value,
                )
              }
            />
          </div>
        </div>

        <div className="mt-3">
          <span className="badge text-bg-light">
            Backend Controlled
          </span>

          <span className="badge text-bg-light ms-2">
            Geography Controlled
          </span>
        </div>
      </div>
    </section>
  );
}
