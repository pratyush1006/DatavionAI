"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { transcriptionApi } from "../api/transcription-api";
import type { GeneratedNote } from "../types";

export function LiveTranscriptionWorkspace({
	sessionId,
	autoStart = false,
}: {
	sessionId: string;
	autoStart?: boolean;
}) {
	const [running, setRunning] = useState(false);
	const [text, setText] = useState("");
	const [error, setError] = useState<string | null>(null);
	const [generatedNote, setGeneratedNote] = useState<GeneratedNote>();
	const [draftText, setDraftText] = useState("");
	const [busy, setBusy] = useState(false);
	const socketRef = useRef<WebSocket | null>(null);
	const recorderRef = useRef<MediaRecorder | null>(null);
	const streamRef = useRef<MediaStream | null>(null);

	const stop = useCallback(() => {
		const recorder = recorderRef.current;
		const socket = socketRef.current;
		if (recorder && recorder.state !== "inactive") {
			recorder.onstop = () => {
				if (socket?.readyState === WebSocket.OPEN) {
					socket.send(JSON.stringify({ type: "session.stop" }));
				}
			};
			recorder.stop();
		} else if (socket?.readyState === WebSocket.OPEN) {
			socket.send(JSON.stringify({ type: "session.stop" }));
		}
		recorderRef.current = null;
		streamRef.current?.getTracks().forEach((track) => track.stop());
		streamRef.current = null;
		setRunning(false);
	}, []);

	const start = useCallback(async () => {
		try {
			const stream = await navigator.mediaDevices.getUserMedia({
				audio: {
					echoCancellation: true,
					noiseSuppression: true,
					autoGainControl: true,
				},
			});
			streamRef.current = stream;
			const { ticket } = await transcriptionApi.createLiveSessionTicket(sessionId);
			const protocol = window.location.protocol === "https:" ? "wss" : "ws";
			const socket = new WebSocket(
				`${protocol}://${window.location.host}/ws/transcription/live/${sessionId}/`,
				["datavion.ticket", ticket],
			);
			socket.binaryType = "arraybuffer";
			socket.onmessage = (event) => {
				const message = JSON.parse(event.data);
				if (message.type === "transcript.segment") {
					setText((value) => value + (value ? " " : "") + message.text);
				}
				if (message.type === "error") {
					setError(message.message || message.code);
				}
					if (message.type === "session.completed") {
						socket.close();
						setBusy(true);
						void transcriptionApi.generateLiveSessionNote(sessionId)
							.then((note) => {
								setGeneratedNote(note);
								setDraftText(note.draft_text);
							})
							.catch((cause) => setError(cause instanceof Error ? cause.message : "Unable to generate the clinical note."))
							.finally(() => setBusy(false));
					}
			};
			socket.onerror = () => setError("Live transcription connection failed.");
			socket.onclose = () => setRunning(false);
			socket.onopen = () => {
				const recorder = new MediaRecorder(stream);
				recorderRef.current = recorder;
				recorder.ondataavailable = (event) => {
					if (event.data.size && socket.readyState === WebSocket.OPEN) {
						socket.send(event.data);
					}
				};
				recorder.start(250);
				setRunning(true);
			};
			socketRef.current = socket;
		} catch (cause) {
			streamRef.current?.getTracks().forEach((track) => track.stop());
			streamRef.current = null;
			setError(cause instanceof Error ? cause.message : "Unable to start microphone capture.");
		}
	}, [sessionId]);

	useEffect(() => {
		const startTimer = autoStart
			? window.setTimeout(() => void start(), 0)
			: undefined;
		return () => {
			if (startTimer !== undefined) window.clearTimeout(startTimer);
			stop();
		};
	}, [autoStart, start, stop]);

	async function saveDraft() {
		if (!generatedNote) return;
		setBusy(true);
		try {
			const note = await transcriptionApi.updateNoteDraft(generatedNote.note_id, draftText);
			setGeneratedNote(note);
		} catch (cause) {
			setError(cause instanceof Error ? cause.message : "Unable to save the note draft.");
		} finally {
			setBusy(false);
		}
	}

	async function approveDraft() {
		if (!generatedNote) return;
		setBusy(true);
		try {
			const saved = await transcriptionApi.updateNoteDraft(generatedNote.note_id, draftText);
			const reviewed = await transcriptionApi.reviewNote(saved.note_id, "approve");
			setGeneratedNote(reviewed);
		} catch (cause) {
			setError(cause instanceof Error ? cause.message : "Unable to verify the note.");
		} finally {
			setBusy(false);
		}
	}

	return (
		<section aria-label="Live clinical transcription" className="space-y-3">
			<div className="flex items-center justify-between">
				<h2 className="font-semibold">AI Scribe · Live transcript</h2>
				<button type="button" onClick={running ? stop : () => void start()}>
					{running ? "Stop recording" : "Start live transcription"}
				</button>
			</div>
			<p className="text-xs text-muted-foreground">
				Browser echo cancellation and noise suppression are enabled when supported.
			</p>
			{error && <p role="alert" className="text-sm text-destructive">{error}</p>}
			<pre className="max-h-72 overflow-auto whitespace-pre-wrap rounded-md border p-3 text-sm">
				{text || "Live transcript will appear here."}
			</pre>
			{busy && <p role="status">Preparing or saving the clinician-reviewable draft…</p>}
			{generatedNote && (
				<div className="space-y-3 rounded-md border p-3">
					<div className="flex items-center justify-between">
						<h3 className="font-medium">AI-generated {generatedNote.note_type} note · {generatedNote.status}</h3>
					</div>
					<textarea
						className="min-h-48 w-full rounded-md border bg-background p-3 text-sm"
						value={draftText}
						disabled={generatedNote.status === "review" || generatedNote.status === "signed"}
						onChange={(event) => setDraftText(event.target.value)}
					/>
					<div className="flex justify-end gap-2">
						<button type="button" disabled={busy || generatedNote.status !== "draft"} onClick={() => void saveDraft()}>Save edits</button>
						<button type="button" disabled={busy || generatedNote.status !== "draft"} onClick={() => void approveDraft()}>Doctor verify</button>
					</div>
				</div>
			)}
		</section>
	);
}
