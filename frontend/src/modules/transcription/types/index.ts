export type TranscriptionStatus =
  | "created"
  | "queued"
  | "processing"
  | "completed"
  | "failed"
  | "cancelled";

export type NoteStatus = "draft" | "review" | "signed" | "rejected";

export interface TranscriptionJob {
  id: string;
  job_id: string;
  organization: string;
  patient: string;
  encounter: string | null;
  created_by: string;
  status: TranscriptionStatus;
  audio_uri: string;
  language: string;
  transcript_text: string;
  transcript_json: Record<string, unknown>;
  duration_seconds: number | null;
  speaker_count: number | null;
  error_code: string;
  error_message: string;
  created_at: string;
  updated_at: string;
}

export interface GeneratedNote {
  id: string;
  note_id: string;
  job: string;
  patient: string;
  encounter: string | null;
  status: NoteStatus;
  note_type: string;
  draft_text: string;
  structured_content: Record<string, unknown>;
  generated_by_provider: string;
  reviewed_by: string | null;
  reviewed_at: string | null;
  signed_at: string | null;
  rejection_reason: string;
}
