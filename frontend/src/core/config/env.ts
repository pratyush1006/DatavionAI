export const env = {
  appName:
    process.env.NEXT_PUBLIC_APP_NAME ??
    "Datavion AI",

  apiBaseUrl:
    process.env.NEXT_PUBLIC_API_BASE_URL ??
    "http://127.0.0.1:8000/api",
} as const;
