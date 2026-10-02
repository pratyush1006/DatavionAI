export type DocumentStatus = 'DRAFT' | 'ACTIVE' | 'ARCHIVED' | 'DELETED' | string;
export type DocumentMediaFamily = 'pdf' | 'image' | 'office' | 'audio' | 'video' | 'unknown';

export interface Document {
  readonly id: string;
  readonly title: string;
  readonly documentType: string;
  readonly status: DocumentStatus;
  readonly accessLevel: string;
  readonly originalFilename: string;
  readonly mimeType: string;
  readonly fileSize: number;
  readonly storageKey: string | null;
  readonly checksum: string | null;
  readonly downloadUrl: string | null;
  readonly metadata: Record<string, unknown>;
  readonly aiMetadata: Record<string, unknown>;
  readonly createdAt: string;
  readonly updatedAt: string;
}

export interface DocumentVersion {
  readonly id: string;
  readonly documentId: string;
  readonly versionNumber: number;
  readonly status: string;
  readonly storageKey: string | null;
  readonly originalFilename: string;
  readonly mimeType: string;
  readonly fileSize: number;
  readonly checksum: string | null;
  readonly createdAt: string;
  readonly updatedAt: string;
}

export interface CreateDocumentPayload {
  readonly title: string;
  readonly documentType: string;
  readonly accessLevel?: string;
  readonly metadata?: Record<string, unknown>;
  readonly aiMetadata?: Record<string, unknown>;
}
export interface UpdateDocumentPayload {
  readonly title?: string;
  readonly documentType?: string;
  readonly accessLevel?: string;
  readonly metadata?: Record<string, unknown>;
  readonly aiMetadata?: Record<string, unknown>;
}
export interface CreateDocumentVersionPayload { readonly file: File; }

export function getDocumentMediaFamily(mime: string, filename: string): DocumentMediaFamily {
  const m = mime.toLowerCase();
  const ext = filename.split('.').pop()?.toLowerCase() ?? '';
  if (m === 'application/pdf' || ext === 'pdf') return 'pdf';
  if (m.startsWith('image/') || ['jpg','jpeg','png','webp','gif','tif','tiff'].includes(ext)) return 'image';
  if (m.startsWith('audio/') || ['mp3','m4a','wav','ogg','flac'].includes(ext)) return 'audio';
  if (m.startsWith('video/') || ['mp4','webm','mov','avi','mpeg','mpg'].includes(ext)) return 'video';
  if (['doc','docx','xls','xlsx','ppt','pptx','odt','ods','odp'].includes(ext)) return 'office';
  return 'unknown';
}
