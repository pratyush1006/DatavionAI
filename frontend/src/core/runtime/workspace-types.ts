export type WorkspaceRuntimeStatus =
  | "loading"
  | "authenticated"
  | "unauthenticated"
  | "error";

export type WorkspaceRuntimeState = {
  status: WorkspaceRuntimeStatus;
  error: Error | null;
  refresh: () => Promise<void>;
  logout: () => Promise<void>;
};
