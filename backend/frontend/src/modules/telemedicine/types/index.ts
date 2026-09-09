export type MediaPermission="prompt"|"granted"|"denied"|"not_applicable";
export type SessionStatus="draft"|"scheduled"|"confirmed"|"ready"|"in_progress"|"completed"|"cancelled"|"no_show"|"failed";
export interface TelemedicineSession { id:string; session_id:string; patient:string; provider:string; appointment:string|null; scheduled_start:string; scheduled_end:string; actual_start:string|null; actual_end:string|null; status:SessionStatus; session_type:"video"|"audio"|"chat"; connection_url:string; connection_id:string; provider_name:string; recording_consent:boolean; }
export interface MediaDeviceOption { deviceId:string; label:string; kind:MediaDeviceKind; }
export interface ParticipantMediaState { microphone_enabled:boolean; camera_enabled:boolean; audio_connected:boolean; video_connected:boolean; microphone_permission:MediaPermission; camera_permission:MediaPermission; }
