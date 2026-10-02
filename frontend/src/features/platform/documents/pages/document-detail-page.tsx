"use client";
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { apiClient } from '@/core/api';
import { DocumentDetails, MediaPreview } from '../components';
import { documentEndpoints } from '../api';
import { useDocumentMutations, useDocumentQuery } from '../hooks';
export function DocumentDetailPage({id}:{id:string}){
  const router=useRouter();
  const q=useDocumentQuery(id);
  const {remove}=useDocumentMutations();
  if(q.isLoading)return <div>Loading document...</div>;
  if(q.isError||!q.data)return <div className="space-y-4"><p className="text-destructive">Unable to load this document.</p><Button asChild variant="outline"><Link href="/documents">Back to Documents</Link></Button></div>;
  const d=q.data;
  const handleDelete=()=>{if(window.confirm('Delete this document?'))remove.mutate(d.id,{onSuccess:()=>router.push('/documents')});};
  const handleDownload=async()=>{const response=await apiClient.get<{url:string}>(documentEndpoints.download(d.id)); window.open(response.data.url,'_blank','noopener,noreferrer');};
  return <div className="space-y-6"><div className="flex flex-wrap items-center justify-between gap-4"><div><h1 className="text-2xl font-semibold">{d.title}</h1><p className="text-sm text-muted-foreground">{d.originalFilename}</p></div><div className="flex gap-2"><Button asChild variant="outline"><Link href="/documents">Back</Link></Button><Button variant="outline" onClick={()=>void handleDownload()}>Download PDF</Button><Button variant="destructive" onClick={handleDelete} disabled={remove.isPending}>{remove.isPending?'Deleting...':'Delete'}</Button></div></div><DocumentDetails document={d}/>{d.downloadUrl&&<MediaPreview document={d} url={d.downloadUrl}/>}</div>
}
