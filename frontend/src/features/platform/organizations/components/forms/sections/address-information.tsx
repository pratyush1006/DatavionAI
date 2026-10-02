/**
 * =============================================================================
 * DatavionOS
 * File:
 * src/features/platform/organizations/components/forms/sections/address-information.tsx
 * =============================================================================
 *
 * Organization address information.
 *
 * Responsibilities
 * ----------------
 * - Render Country -> Region -> City Geography selectors.
 * - Load Geography data through the platform Geography query layer.
 * - Cascade dependent Geography selections.
 * - Synchronize canonical Geography references with legacy display fields.
 * - Populate timezone from the selected city when appropriate.
 * - Preserve edit-form hydration without clearing existing selections.
 * =============================================================================
 */

"use client";

import {
  useEffect,
  useRef,
} from "react";

import type {
  UseFormReturn,
} from "react-hook-form";

import {
  ControlledInput,
  ControlledSelect,
  ControlledTextarea,
  FormGrid,
  FormSection,
  type SelectOption,
} from "@/components/common/forms";

import {
  useCitiesQuery,
  useCountriesQuery,
  useRegionsQuery,
} from "@/features/platform/geography/hooks";

import type {
  OrganizationFormValues,
} from "../../../domain";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type AddressInformationProps =
  Readonly<{
    form:
      UseFormReturn<OrganizationFormValues>;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function AddressInformation({
  form,
}: AddressInformationProps) {
  /**
   * Canonical Geography selections.
   *
   * ControlledSelect is already integrated with React Hook Form, so we observe
   * these values rather than passing unsupported change handlers to it.
   */
  const countryRef =
    form.watch("countryRef");

  const regionRef =
    form.watch("regionRef");

  const cityRef =
    form.watch("cityRef");

  /**
   * Capture the initial hierarchy so edit-form hydration does not immediately
   * clear the server-provided Region and City values.
   */
  const previousCountryRef =
    useRef<string | null>(
      countryRef ?? null,
    );

  const previousRegionRef =
    useRef<string | null>(
      regionRef ?? null,
    );

  /* ===========================================================================
   * Geography queries
   * =========================================================================== */

  const {
    data: countries = [],
    isPending: countriesLoading,
  } =
    useCountriesQuery();

  const {
    data: regions = [],
    isPending: regionsLoading,
    isFetching: regionsFetching,
  } =
    useRegionsQuery(
      countryRef ?? "",
    );

  const {
    data: cities = [],
    isPending: citiesLoading,
    isFetching: citiesFetching,
  } =
    useCitiesQuery(
      regionRef ?? "",
    );

  /* ===========================================================================
   * Options
   * =========================================================================== */

  const countryOptions:
    SelectOption[] =
    countries.map(
      (country) => ({
        value: country.id,
        label: country.name,
      }),
    );

  const regionOptions:
    SelectOption[] =
    regions.map(
      (region) => ({
        value: region.id,
        label: region.name,
      }),
    );

  const cityOptions:
    SelectOption[] =
    cities.map(
      (city) => ({
        value: city.id,
        label: city.name,
      }),
    );

  /* ===========================================================================
   * Country synchronization
   * =========================================================================== */

  /**
   * Keep the legacy country string synchronized with the canonical Country
   * reference.
   *
   * When the user changes Country, all descendant Geography selections become
   * invalid and must be cleared.
   *
   * The initial render is intentionally excluded from the cascade so existing
   * edit-form values can hydrate correctly.
   */
  useEffect(() => {
    const currentCountryRef =
      countryRef ?? null;

    const previousCountry =
      previousCountryRef.current;

    const countryChanged =
      currentCountryRef !==
      previousCountry;

    previousCountryRef.current =
      currentCountryRef;

    if (!currentCountryRef) {
      if (previousCountry !== null) {
        form.setValue(
          "country",
          "",
          {
            shouldDirty: true,
            shouldValidate: true,
          },
        );

        form.setValue(
          "regionRef",
          null,
          {
            shouldDirty: true,
            shouldValidate: true,
          },
        );

        form.setValue(
          "cityRef",
          null,
          {
            shouldDirty: true,
            shouldValidate: true,
          },
        );

        form.setValue(
          "state",
          "",
          {
            shouldDirty: true,
            shouldValidate: true,
          },
        );

        form.setValue(
          "city",
          "",
          {
            shouldDirty: true,
            shouldValidate: true,
          },
        );
      }

      return;
    }

    const country =
      countries.find(
        (item) =>
          item.id === currentCountryRef,
      );

    if (country) {
      form.setValue(
        "country",
        country.name,
        {
          shouldDirty: countryChanged,
          shouldValidate: true,
        },
      );
    }

    /**
     * Do not cascade on initial hydration.
     */
    if (!countryChanged) {
      return;
    }

    form.setValue(
      "regionRef",
      null,
      {
        shouldDirty: true,
        shouldValidate: true,
      },
    );

    form.setValue(
      "cityRef",
      null,
      {
        shouldDirty: true,
        shouldValidate: true,
      },
    );

    form.setValue(
      "state",
      "",
      {
        shouldDirty: true,
        shouldValidate: true,
      },
    );

    form.setValue(
      "city",
      "",
      {
        shouldDirty: true,
        shouldValidate: true,
      },
    );
  }, [
    countryRef,
    countries,
    form,
  ]);

  /* ===========================================================================
   * Region synchronization
   * =========================================================================== */

  /**
   * Keep the legacy state string synchronized with the canonical Region
   * reference.
   *
   * When Region changes, City becomes invalid and is cleared.
   *
   * As with Country, the initial edit-form hierarchy is preserved.
   */
  useEffect(() => {
    const currentRegionRef =
      regionRef ?? null;

    const previousRegion =
      previousRegionRef.current;

    const regionChanged =
      currentRegionRef !==
      previousRegion;

    previousRegionRef.current =
      currentRegionRef;

    if (!currentRegionRef) {
      if (previousRegion !== null) {
        form.setValue(
          "state",
          "",
          {
            shouldDirty: true,
            shouldValidate: true,
          },
        );

        form.setValue(
          "cityRef",
          null,
          {
            shouldDirty: true,
            shouldValidate: true,
          },
        );

        form.setValue(
          "city",
          "",
          {
            shouldDirty: true,
            shouldValidate: true,
          },
        );
      }

      return;
    }

    const region =
      regions.find(
        (item) =>
          item.id === currentRegionRef,
      );

    if (region) {
      form.setValue(
        "state",
        region.name,
        {
          shouldDirty: regionChanged,
          shouldValidate: true,
        },
      );
    }

    /**
     * Do not cascade on initial hydration.
     */
    if (!regionChanged) {
      return;
    }

    form.setValue(
      "cityRef",
      null,
      {
        shouldDirty: true,
        shouldValidate: true,
      },
    );

    form.setValue(
      "city",
      "",
      {
        shouldDirty: true,
        shouldValidate: true,
      },
    );
  }, [
    regionRef,
    regions,
    form,
  ]);

  /* ===========================================================================
   * City synchronization
   * =========================================================================== */

  /**
   * Keep the legacy city string synchronized with the canonical City reference.
   *
   * The city's authoritative timezone is also used to populate the organization
   * timezone when the timezone field has not already been manually changed.
   */
  useEffect(() => {
    if (!cityRef) {
      return;
    }

    const city =
      cities.find(
        (item) =>
          item.id === cityRef,
      );

    if (!city) {
      return;
    }

    form.setValue(
      "city",
      city.name,
      {
        shouldDirty: false,
        shouldValidate: true,
      },
    );

    if (
      city.timezone &&
      !form.getFieldState(
        "timezone",
      ).isDirty
    ) {
      form.setValue(
        "timezone",
        city.timezone,
        {
          shouldDirty: false,
          shouldValidate: true,
        },
      );
    }
  }, [
    cityRef,
    cities,
    form,
  ]);

  /* ===========================================================================
   * Render
   * =========================================================================== */

  return (
    <FormSection
      title="Address"
      description="Location information for the organization."
    >
      <FormGrid>
        <ControlledSelect
          form={form}
          name="countryRef"
          label="Country"
          placeholder={
            countriesLoading
              ? "Loading countries..."
              : "Select country"
          }
          options={countryOptions}
          disabled={
            countriesLoading
          }
          required
        />

        <ControlledSelect
          form={form}
          name="regionRef"
          label="State / Region"
          placeholder={
            !countryRef
              ? "Select country first"
              : regionsLoading ||
                  regionsFetching
                ? "Loading states..."
                : regionOptions.length === 0
                  ? "No states available"
                  : "Select state / region"
          }
          options={regionOptions}
          disabled={
            !countryRef ||
            regionsLoading ||
            regionsFetching ||
            regionOptions.length === 0
          }
          required
        />

        <ControlledSelect
          form={form}
          name="cityRef"
          label="City"
          placeholder={
            !regionRef
              ? "Select state / region first"
              : citiesLoading ||
                  citiesFetching
                ? "Loading cities..."
                : cityOptions.length === 0
                  ? "No cities available"
                  : "Select city"
          }
          options={cityOptions}
          disabled={
            !regionRef ||
            citiesLoading ||
            citiesFetching ||
            cityOptions.length === 0
          }
          required
        />

        <ControlledInput
          form={form}
          name="postalCode"
          label="Postal Code"
          placeholder="560001"
          required
          autoComplete="postal-code"
        />

        <ControlledTextarea
          form={form}
          name="address"
          label="Address"
          placeholder="Enter the complete organization address"
          rows={4}
          required
          className="lg:col-span-2"
        />
      </FormGrid>
    </FormSection>
  );
}
