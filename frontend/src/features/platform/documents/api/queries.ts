import { queryOptions } from '@tanstack/react-query';
import { apiClient } from '@/core/api';
import type { Document, DocumentVersion } from '../domain';
import { documentEndpoints } from './endpoints';
import { documentKeys } from './keys';

type DocumentDto = {
  id: string; title: string; document_type: string; status: string; access_level: string;
  original_filename: string; mime_type: string; file_size: number; storage_key?: string | null;
  checksum?: string | null; url?: string | null; download_url?: string | null; metadata?: Record<string, unknown> | null; ai_metadata?: Record<string, unknown> | null;
  created_at: string; updated_at: string;
};
type VersionDto = {
  id: string; document_id?: string; version_number: number; status: string; storage_key?: string | null;
  original_filename: string; mime_type: string; file_size: number; checksum?: string | null; created_at: string; updated_at: string;
};
const mapDocument = (d: DocumentDto): Document => ({
  id:d.id, title:d.title, documentType:d.document_type, status:d.status, accessLevel:d.access_level,
  originalFilename:d.original_filename, mimeType:d.mime_type, fileSize:d.file_size, storageKey:d.storage_key ?? null,
  checksum:d.checksum ?? null, downloadUrl:d.download_url ?? d.url ?? null, metadata:d.metadata ?? {}, aiMetadata:d.ai_metadata ?? {}, createdAt:d.created_at, updatedAt:d.updated_at,
});
const mapVersion = (d: VersionDto, documentId: string): DocumentVersion => ({
  id:d.id, documentId:d.document_id ?? documentId, versionNumber:d.version_number, status:d.status,
  storageKey:d.storage_key ?? null, originalFilename:d.original_filename, mimeType:d.mime_type, fileSize:d.file_size,
  checksum:d.checksum ?? null, createdAt:d.created_at, updatedAt:d.updated_at,
});
async function fetchDocuments() { const r = await apiClient.get<DocumentDto[]>(documentEndpoints.collection); return r.data.map(mapDocument); }
async function fetchDocument(id: string) { const r = await apiClient.get<DocumentDto>(documentEndpoints.byId(id)); return mapDocument(r.data); }
async function fetchVersions(id: string) { const r = await apiClient.get<VersionDto[]>(documentEndpoints.versions(id)); return r.data.map(v => mapVersion(v, id)); }
export const documentQueries = {
  all: () => queryOptions({ queryKey: documentKeys.lists(), queryFn: fetchDocuments }),
  detail: (id: string) => queryOptions({ queryKey: documentKeys.detail(id), queryFn: () => fetchDocument(id), enabled: id.trim().length > 0 }),
  versions: (id: string) => queryOptions({ queryKey: documentKeys.versions(id), queryFn: () => fetchVersions(id), enabled: id.trim().length > 0 }),
} as const;
