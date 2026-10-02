"use client";

import { useEffect, useState } from "react";

import { BackendSelect } from "./BackendSelect";
import {
  getCities,
  getCountries,
  getDistricts,
  getStates,
} from "@/lib/backend/metadata";
import type { LocationOption } from "@/lib/backend/types";

export type LocationValue = {
  country: string;
  state: string;
  district: string;
  city: string;
  postalCode: string;
};

type Props = {
  value: LocationValue;
  onChange: (value: LocationValue) => void;
  required?: boolean;
};

export function LocationSelector({
  value,
  onChange,
  required,
}: Props) {
  const [countries, setCountries] = useState<LocationOption[]>([]);
  const [states, setStates] = useState<LocationOption[]>([]);
  const [districts, setDistricts] = useState<LocationOption[]>([]);
  const [cities, setCities] = useState<LocationOption[]>([]);

  useEffect(() => {
    let active = true;

    void getCountries()
      .then((items) => {
        if (active) {
          setCountries(items);
        }
      })
      .catch(() => {
        if (active) {
          setCountries([]);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;

    if (!value.country) {
      return () => {
        active = false;
      };
    }

    void getStates(value.country)
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
  }, [value.country]);

  useEffect(() => {
    let active = true;

    if (!value.state) {
      return () => {
        active = false;
      };
    }

    void getDistricts(value.state)
      .then((items) => {
        if (active) {
          setDistricts(items);
        }
      })
      .catch(() => {
        if (active) {
          setDistricts([]);
        }
      });

    return () => {
      active = false;
    };
  }, [value.state]);

  useEffect(() => {
    let active = true;

    if (!value.district) {
      return () => {
        active = false;
      };
    }

    void getCities(value.district)
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
  }, [value.district]);

  const patch = (next: Partial<LocationValue>) => {
    onChange({
      ...value,
      ...next,
    });
  };

  const visibleStates = value.country ? states : [];
  const visibleDistricts = value.state ? districts : [];
  const visibleCities = value.district ? cities : [];

  return (
    <div className="row">
      <div className="col-md-6">
        <BackendSelect
          id="country"
          name="country"
          label="Country"
          value={value.country}
          options={countries}
          onChange={(country) =>
            patch({
              country,
              state: "",
              district: "",
              city: "",
            })
          }
          required={required}
        />
      </div>

      <div className="col-md-6">
        <BackendSelect
          id="state"
          name="state"
          label="State / Region"
          value={value.state}
          options={visibleStates}
          onChange={(state) =>
            patch({
              state,
              district: "",
              city: "",
            })
          }
          disabled={!value.country}
          required={required}
        />
      </div>

      <div className="col-md-6">
        <BackendSelect
          id="district"
          name="district"
          label="District"
          value={value.district}
          options={visibleDistricts}
          onChange={(district) =>
            patch({
              district,
              city: "",
            })
          }
          disabled={!value.state}
          required={required}
        />
      </div>

      <div className="col-md-6">
        <BackendSelect
          id="city"
          name="city"
          label="City"
          value={value.city}
          options={visibleCities}
          onChange={(city) =>
            patch({
              city,
            })
          }
          disabled={!value.district}
          required={required}
        />
      </div>

      <div className="col-md-6">
        <label
          htmlFor="postalCode"
          className="form-label fw-semibold"
        >
          Postal / PIN Code
        </label>

        <input
          id="postalCode"
          name="postalCode"
          className="form-control"
          value={value.postalCode}
          onChange={(event) =>
            patch({
              postalCode: event.target.value,
            })
          }
          inputMode="numeric"
        />
      </div>
    </div>
  );
}
