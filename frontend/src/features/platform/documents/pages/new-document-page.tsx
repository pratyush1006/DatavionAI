"use client";
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useDocumentMutations } from '../hooks';
export function NewDocumentPage(){
  const router=useRouter(); const {upload}=useDocumentMutations();
  const [title,setTitle]=useState(''); const [type,setType]=useState('general'); const [access,setAccess]=useState('private'); const [file,setFile]=useState<File|null>(null);
  const submit=(e:React.FormEvent)=>{e.preventDefault(); if(!title.trim()||!file) return; upload.mutate({title:title.trim(),documentType:type.trim()||'general',accessLevel:access,file},{onSuccess:d=>router.push(`/documents/${d.id}`)});};
  return <form onSubmit={submit} className="max-w-xl space-y-6"><div><h1 className="text-2xl font-semibold">Upload document</h1><p className="mt-1 text-sm text-muted-foreground">Upload a PDF or other supported document. Storage, checksum and download access are enforced by the backend.</p></div><div className="space-y-2"><Label htmlFor="document-file">File</Label><Input id="document-file" type="file" accept="application/pdf,.pdf" onChange={e=>setFile(e.target.files?.[0]??null)} required /></div><div className="space-y-2"><Label htmlFor="document-title">Title</Label><Input id="document-title" value={title} onChange={e=>setTitle(e.target.value)} required /></div><div className="space-y-2"><Label htmlFor="document-type">Document type</Label><Input id="document-type" value={type} onChange={e=>setType(e.target.value)} required /></div><div className="space-y-2"><Label htmlFor="document-access">Access level</Label><select id="document-access" className="h-10 w-full rounded-md border bg-background px-3 text-sm" value={access} onChange={e=>setAccess(e.target.value)}><option value="private">Private</option><option value="organization">Organization</option><option value="tenant">Tenant</option></select></div>{upload.isError&&<p className="text-sm text-destructive">Unable to upload the document.</p>}<Button type="submit" disabled={upload.isPending}>{upload.isPending?'Uploading...':'Upload document'}</Button></form>;
}
