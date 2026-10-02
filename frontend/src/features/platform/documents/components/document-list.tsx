"use client";
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useDocumentsQuery } from '../hooks';
export function DocumentList(){
  const q=useDocumentsQuery();
  if(q.isLoading)return <Card><CardContent className="p-6">Loading documents...</CardContent></Card>;
  if(q.isError)return <Card><CardContent className="p-6 text-destructive">Unable to load documents.</CardContent></Card>;
  const docs=q.data??[];
  return <Card><CardHeader className="flex flex-row items-center justify-between"><CardTitle>Documents</CardTitle><Button asChild><Link href="/documents/new">New document</Link></Button></CardHeader><CardContent className="space-y-2">{docs.length===0?<div className="rounded-md border p-8 text-center text-sm text-muted-foreground">No documents found.</div>:docs.map(d=><Link key={d.id} href={`/documents/${d.id}`} className="block rounded-md border p-4 hover:bg-muted"><div className="flex justify-between gap-4"><div><div className="font-medium">{d.title}</div><div className="text-sm text-muted-foreground">{d.originalFilename} · {d.documentType}</div></div><div className="text-right text-sm"><div>{d.status}</div><div className="text-muted-foreground">{d.accessLevel}</div></div></div></Link>)}</CardContent></Card>;
}
