"use client";
import { LiveTranscriptionWorkspace } from "./LiveTranscriptionWorkspace";
export function DeviceTranscriptionWorkspace({sessionId,deviceId}:{sessionId:string;deviceId:string}) { return <section data-device-id={deviceId}><LiveTranscriptionWorkspace sessionId={sessionId}/></section>; }
