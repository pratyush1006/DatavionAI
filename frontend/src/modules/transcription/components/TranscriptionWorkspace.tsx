"use client";

import { useState } from "react";
import { transcriptionApi } from "../api/transcription-api";
import type { TranscriptionJob } from "../types";
import { TranscriptViewer } from "./TranscriptViewer";

export function TranscriptionWorkspace({
  job,
}: {
  job: TranscriptionJob;
}) {
  const [current, setCurrent] = useState(job);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    try {
      setError(null);
      setCurrent(await transcriptionApi.action(job.job_id, "run"));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to process job.");
    }
  }

  return (
    <section aria-label="Transcription workspace">
      <h2>Clinical transcription</h2>
      <p>Status: {current.status}</p>
      <button type="button" onClick={() => void run()}>
        Run transcription
      </button>
      {error && <p role="alert">{error}</p>}
      <TranscriptViewer text={current.transcript_text} />
    </section>
  );
}
