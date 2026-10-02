"use client";

export function TranscriptViewer({
  text,
}: {
  text: string;
}) {
  return (
    <article aria-label="Transcript">
      <pre style={{ whiteSpace: "pre-wrap" }}>{text}</pre>
    </article>
  );
}
