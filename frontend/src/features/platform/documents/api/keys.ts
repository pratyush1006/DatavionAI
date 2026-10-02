export const documentKeys = {
  all: ['documents'] as const,
  lists: () => [...documentKeys.all, 'list'] as const,
  detail: (id: string) => [...documentKeys.all, 'detail', id] as const,
  versions: (id: string) => [...documentKeys.all, 'versions', id] as const,
} as const;
