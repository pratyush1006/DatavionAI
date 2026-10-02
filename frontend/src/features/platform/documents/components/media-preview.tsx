"use client";
import type { Document } from '../domain';
import { getDocumentMediaFamily } from '../domain';
export function MediaPreview({document,url}:{document:Document;url:string}){
  const f=getDocumentMediaFamily(document.mimeType,document.originalFilename);
  if(f==='image')return (
    // eslint-disable-next-line @next/next/no-img-element -- URL is supplied by the backend storage service.
    <img src={url} alt={document.title} className="max-h-[600px] max-w-full rounded-md object-contain"/>
  );
  if(f==='video')return <video controls preload="metadata" src={url} className="max-h-[600px] max-w-full rounded-md"/>;
  if(f==='audio')return <audio controls preload="metadata" src={url} className="w-full"/>;
  if(f==='pdf')return <iframe title={document.title} src={url} className="h-[700px] w-full rounded-md border"/>;
  return <a href={url} target="_blank" rel="noreferrer" className="underline">Open document</a>;
}
