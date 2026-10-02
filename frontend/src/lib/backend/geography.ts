import { ENDPOINTS } from "./endpoints";
import {
  apiPublicGet,
  apiPublicRequest,
} from "./http";
import type {
  CurrentLocationResult,
  GeographyCity,
  GeographyCountry,
  GeographyRegion,
} from "./contracts";

// Fixtures preserve local development ergonomics only. Production geography
// must always come from the backend master-data and reverse-geocoding APIs.
const allowDevelopmentFallback = process.env.NODE_ENV !== "production";

const FALLBACK_COUNTRIES: GeographyCountry[] = [
  { id: "india", code: "IN", name: "India", iso3: "IND", phone_code: "+91" },
  { id: "usa", code: "US", name: "United States", iso3: "USA", phone_code: "+1" },
  { id: "uk", code: "GB", name: "United Kingdom", iso3: "GBR", phone_code: "+44" },
  { id: "uae", code: "AE", name: "United Arab Emirates", iso3: "ARE", phone_code: "+971" },
  { id: "saudi-arabia", code: "SA", name: "Saudi Arabia", iso3: "SAU", phone_code: "+966" },
  { id: "singapore", code: "SG", name: "Singapore", iso3: "SGP", phone_code: "+65" },
  { id: "australia", code: "AU", name: "Australia", iso3: "AUS", phone_code: "+61" },
];

const FALLBACK_REGIONS: Record<string, GeographyRegion[]> = {
  india: [
    { id: "karnataka", country: "india", code: "KA", name: "Karnataka", region_type: "state" },
    { id: "maharashtra", country: "india", code: "MH", name: "Maharashtra", region_type: "state" },
    { id: "delhi", country: "india", code: "DL", name: "Delhi", region_type: "state" },
  ],
  usa: [
    { id: "california", country: "usa", code: "CA", name: "California", region_type: "state" },
    { id: "new-york", country: "usa", code: "NY", name: "New York", region_type: "state" },
    { id: "texas", country: "usa", code: "TX", name: "Texas", region_type: "state" },
  ],
};

const FALLBACK_CITIES: Record<string, GeographyCity[]> = {
  karnataka: [
    { id: "bangalore", country: "india", region: "karnataka", name: "Bangalore", latitude: 12.9716, longitude: 77.5946, timezone: "Asia/Kolkata" },
    { id: "mysuru", country: "india", region: "karnataka", name: "Mysuru", latitude: 12.2958, longitude: 76.6394, timezone: "Asia/Kolkata" },
  ],
  maharashtra: [
    { id: "mumbai", country: "india", region: "maharashtra", name: "Mumbai", latitude: 19.076, longitude: 72.8777, timezone: "Asia/Kolkata" },
    { id: "pune", country: "india", region: "maharashtra", name: "Pune", latitude: 18.5204, longitude: 73.8567, timezone: "Asia/Kolkata" },
  ],
  delhi: [
    { id: "new-delhi", country: "india", region: "delhi", name: "New Delhi", latitude: 28.6139, longitude: 77.209, timezone: "Asia/Kolkata" },
  ],
  california: [
    { id: "san-francisco", country: "usa", region: "california", name: "San Francisco", latitude: 37.7749, longitude: -122.4194, timezone: "America/Los_Angeles" },
    { id: "los-angeles", country: "usa", region: "california", name: "Los Angeles", latitude: 34.0522, longitude: -118.2437, timezone: "America/Los_Angeles" },
  ],
};

export async function getCountries(): Promise<GeographyCountry[]> {
  try {
    const response = await apiPublicGet<GeographyCountry[]>(
      ENDPOINTS.geography.countries,
    );
    if (response.data && response.data.length > 0) {
      return response.data;
    }
  } catch {
    // Fall through to a resilient fallback list below.
  }

  if (allowDevelopmentFallback) {
    return FALLBACK_COUNTRIES;
  }

  throw new Error("Unable to load countries from DatavionOS geography.");
}

export async function getRegions(
  countryId: string,
): Promise<GeographyRegion[]> {
  try {
    const response = await apiPublicGet<GeographyRegion[]>(
      `${ENDPOINTS.geography.regions}?country=${encodeURIComponent(countryId)}`,
    );
    if (response.data && response.data.length > 0) {
      return response.data;
    }
  } catch {
    // Fall through to the fallback regions.
  }

  if (allowDevelopmentFallback) {
    const key = String(countryId).toLowerCase();
    return FALLBACK_REGIONS[key] ?? [];
  }

  throw new Error("Unable to load regions from DatavionOS geography.");
}

export async function getCities(
  regionId: string,
): Promise<GeographyCity[]> {
  try {
    const response = await apiPublicGet<GeographyCity[]>(
      `${ENDPOINTS.geography.cities}?region=${encodeURIComponent(regionId)}`,
    );
    if (response.data && response.data.length > 0) {
      return response.data;
    }
  } catch {
    // Fall through to the fallback cities.
  }

  if (allowDevelopmentFallback) {
    const key = String(regionId).toLowerCase();
    return FALLBACK_CITIES[key] ?? [];
  }

  throw new Error("Unable to load cities from DatavionOS geography.");
}

export async function getCurrentLocation(
  latitude: number,
  longitude: number,
  accuracyMeters?: number | null,
): Promise<CurrentLocationResult> {
  try {
    return await apiPublicRequest<CurrentLocationResult>(
      ENDPOINTS.geography.currentLocation,
      {
        method: "POST",
        body: JSON.stringify({
          latitude,
          longitude,
          accuracy_meters: accuracyMeters ?? null,
        }),
      },
    );

  } catch (reason) {
    if (!allowDevelopmentFallback) {
      throw new Error(
        "Unable to resolve the current location from DatavionOS geography.",
        { cause: reason },
      );
    }
  }

  return {
    latitude,
    longitude,
    accuracy_meters: accuracyMeters ?? null,
    formatted_address: "Current device location",
    country: "India",
    country_code: "IN",
    state: "Karnataka",
    district: "Bengaluru",
    city: "Bangalore",
    postal_code: "",
    timezone: "Asia/Kolkata",
    provider: "development-fixture",
    reference: { lat: latitude, lon: longitude },
  };
}
