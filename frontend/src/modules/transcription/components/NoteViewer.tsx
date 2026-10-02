"use client";

import type { GeneratedNote } from "../types";

export function NoteViewer({ note }: { note: GeneratedNote }) {
  return (
    <article aria-label="Generated clinical note">
      <header>
        <strong>{note.note_type.toUpperCase()}</strong>
        <span>{note.status}</span>
      </header>
      <pre style={{ whiteSpace: "pre-wrap" }}>{note.draft_text}</pre>
    </article>
  );
}
