import { API_BASE_URL } from "@/core/api/config";
export const env = {
  appName:
    process.env.NEXT_PUBLIC_APP_NAME ??
    "Datavion AI",

  apiBaseUrl:
    API_BASE_URL,
} as const;
