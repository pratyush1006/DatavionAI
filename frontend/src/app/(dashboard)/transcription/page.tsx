"use client";

import { useEffect, useState } from "react";
import { transcriptionApi } from "@/modules/transcription";
import type { TranscriptionJob } from "@/modules/transcription";

export default function TranscriptionPage() {
  const [jobs, setJobs] = useState<TranscriptionJob[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    transcriptionApi
      .listJobs()
      .then(setJobs)
      .catch((err) =>
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load transcription jobs."
        )
      );
  }, []);

  return (
    <main>
      <h1>Clinical Transcription</h1>
      {error && <p role="alert">{error}</p>}
      <section>
        {jobs.map((job) => (
          <article key={job.job_id}>
            <strong>{job.status}</strong>
            <p>{job.transcript_text || "Transcript pending."}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
