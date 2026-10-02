"use client";
import { useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { getDocumentMediaFamily } from '../domain';
import { useDocumentMutations } from '../hooks';
export function DocumentUpload({documentId}:{documentId:string}){
  const ref=useRef<HTMLInputElement>(null); const [error,setError]=useState<string|null>(null); const {createVersion}=useDocumentMutations();
  const submit=()=>{const file=ref.current?.files?.[0]; if(!file){setError('Select a file first.');return;} if(getDocumentMediaFamily(file.type,file.name)==='unknown'){setError('Unsupported document media type.');return;} setError(null); createVersion.mutate({documentId,payload:{file}});};
  return <div className="space-y-3"><Label htmlFor="document-file">Upload new version</Label><Input id="document-file" ref={ref} type="file" accept=".pdf,.jpg,.jpeg,.png,.webp,.gif,.tif,.tiff,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.odt,.ods,.odp,.mp3,.m4a,.wav,.ogg,.flac,.mp4,.webm,.mov,.avi,.mpeg,.mpg" />{error&&<p className="text-sm text-destructive">{error}</p>}<Button onClick={submit} disabled={createVersion.isPending}>{createVersion.isPending?'Uploading...':'Upload version'}</Button></div>;
}
