import {apiClient,unwrapData} from "@/core/api";
import type {ParticipantMediaState,TelemedicineSession} from "../types";
const BASE="/api/telemedicine";
export const telemedicineApi={listSessions:async()=>unwrapData(await apiClient.get<TelemedicineSession[]>(`${BASE}/sessions/`)),getSession:async(id:string)=>unwrapData(await apiClient.get<TelemedicineSession>(`${BASE}/sessions/${id}/`)),action:async(id:string,a:string,b:Record<string,unknown>={})=>unwrapData(await apiClient.post<TelemedicineSession>(`${BASE}/sessions/${id}/${a}/`,b)),updateParticipantMedia:async(id:string,s:ParticipantMediaState)=>unwrapData(await apiClient.patch(`${BASE}/participants/${id}/media-state/`,s))};
