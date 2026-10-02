"use client";

import React, { useEffect, useState } from "react";
import { ClinicalNote, NotesApi } from "./api";

export function ClinicalNotesWorkspace() {
  const [notes, setNotes] = useState<ClinicalNote[]>([]);
  const [selected, setSelected] = useState<ClinicalNote | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    NotesApi.list()
      .then(setNotes)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-6">Loading Clinical Notes…</div>;
  }

  return (
    <div className="grid grid-cols-1 gap-6 p-6 lg:grid-cols-3">
      <section className="lg:col-span-1">
        <div className="rounded-lg border bg-white">
          <div className="border-b p-4 font-semibold">Clinical Notes</div>
          <div className="divide-y">
            {notes.length === 0 ? (
              <div className="p-4 text-sm text-muted-foreground">
                No clinical notes found.
              </div>
            ) : (
              notes.map((note) => (
                <button
                  key={`${note.title || "clinical-note"}-${notes.indexOf(note)}`}
                  type="button"
                  onClick={() => setSelected(note)}
                  className="block w-full p-4 text-left hover:bg-muted"
                >
                  <div className="font-medium">
                    {note.title || "Untitled note"}
                  </div>
                  <div className="mt-1 text-sm text-muted-foreground">
                    {note.note_type || "Clinical note"}
                  </div>
                </button>
              ))
            )}
          </div>
        </div>
      </section>

      <section className="lg:col-span-2">
        <div className="rounded-lg border bg-white p-6">
          {selected ? (
            <>
              <h2 className="text-xl font-semibold">
                {selected.title || "Untitled note"}
              </h2>
              <div className="mt-4 whitespace-pre-wrap text-sm">
                {JSON.stringify(selected, null, 2)}
              </div>
            </>
          ) : (
            <div className="text-sm text-muted-foreground">
              Select a clinical note to view its contents.
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
