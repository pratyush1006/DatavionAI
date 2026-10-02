import { apiClient, unwrapData } from "@/core/api";
import type { GeneratedNote, TranscriptionJob } from "../types";

const BASE = "/api/transcription";

export const transcriptionApi = {
  createLiveSessionTicket: async (sessionId: string) =>
    unwrapData(
      await apiClient.post<{ ticket: string }>(
        `${BASE}/live-sessions/${sessionId}/ticket/`
      )
    ),

  generateLiveSessionNote: async (sessionId: string, noteType = "soap") =>
    unwrapData(
      await apiClient.post<GeneratedNote>(
        `${BASE}/live-sessions/${sessionId}/notes/generate/`,
        { note_type: noteType }
      )
    ),

  updateNoteDraft: async (noteId: string, draftText: string) =>
    unwrapData(
      await apiClient.patch<GeneratedNote>(
        `${BASE}/notes/${noteId}/`,
        { draft_text: draftText }
      )
    ),

  listJobs: async () =>
    unwrapData(await apiClient.get<TranscriptionJob[]>(`${BASE}/jobs/`)),

  getJob: async (jobId: string) =>
    unwrapData(
      await apiClient.get<TranscriptionJob>(`${BASE}/jobs/${jobId}/`)
    ),

  action: async (
    jobId: string,
    action: "queue" | "run" | "cancel"
  ) =>
    unwrapData(
      await apiClient.post<TranscriptionJob>(
        `${BASE}/jobs/${jobId}/${action}/`
      )
    ),

  generateNote: async (jobId: string, noteType = "soap") =>
    unwrapData(
      await apiClient.post<GeneratedNote>(
        `${BASE}/jobs/${jobId}/notes/generate/`,
        { note_type: noteType }
      )
    ),

  getNote: async (noteId: string) =>
    unwrapData(
      await apiClient.get<GeneratedNote>(`${BASE}/notes/${noteId}/`)
    ),

  reviewNote: async (
    noteId: string,
    decision: "approve" | "reject",
    rejectionReason = ""
  ) =>
    unwrapData(
      await apiClient.post<GeneratedNote>(
        `${BASE}/notes/${noteId}/review/`,
        {
          decision,
          rejection_reason: rejectionReason,
        }
      )
    ),

  signNote: async (noteId: string) =>
    unwrapData(
      await apiClient.post<GeneratedNote>(
        `${BASE}/notes/${noteId}/sign/`
      )
    ),
};
