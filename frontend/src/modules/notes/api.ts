export type ClinicalNoteStatus = "draft" | "in_review" | "signed" | "amended" | "cancelled";
export type ClinicalNote = { note_id: string; title: string; body: string; status: ClinicalNoteStatus; note_type: string; source: string; version: number; patient: string; encounter: string | null; };

const base = "/api/notes";
export const NotesApi = {
  list: async (): Promise<ClinicalNote[]> => (await fetch(`${base}/`, { credentials: "include" })).json(),
  get: async (id: string): Promise<ClinicalNote> => (await fetch(`${base}/${id}/`, { credentials: "include" })).json(),
  create: async (payload: Record<string, unknown>): Promise<ClinicalNote> => (await fetch(`${base}/`, { method: "POST", credentials: "include", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })).json(),
  action: async (id: string, action: "review" | "sign" | "cancel", payload: Record<string, unknown> = {}): Promise<ClinicalNote> => (await fetch(`${base}/${id}/${action}/`, { method: "POST", credentials: "include", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })).json(),
};
