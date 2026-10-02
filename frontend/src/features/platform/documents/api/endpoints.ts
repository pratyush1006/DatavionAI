const BASE_ENDPOINT = '/documents/';
export const documentEndpoints = {
  base: BASE_ENDPOINT,
  collection: BASE_ENDPOINT,
  upload: `${BASE_ENDPOINT}upload/`,
  byId: (id: string) => `${BASE_ENDPOINT}${encodeURIComponent(id)}/`,
  download: (id: string) => `${BASE_ENDPOINT}${encodeURIComponent(id)}/download/`,
  versions: (id: string) => `${BASE_ENDPOINT}${encodeURIComponent(id)}/versions/`,
} as const;
