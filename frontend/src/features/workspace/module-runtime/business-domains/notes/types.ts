export type NotesRecord = {
  id?: string | number;
  uuid?: string;
  title?: string;
  status?: string;
  patient?: string;
  patient_name?: string;
  encounter?: string;
  encounter_id?: string;
  author?: string;
  author_name?: string;
  note_type?: string;
  created_at?: string;
  updated_at?: string;
  finalized_at?: string;
  [key: string]: unknown;
};

export type NotesWorkspaceProps = {
  module: import("../../domain/types").ModuleRuntimeDefinition;
};
