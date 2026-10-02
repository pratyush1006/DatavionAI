import { DocumentDetailPage } from '@/features/platform/documents';
export default async function Page({params}:{params:Promise<{id:string}>}){const {id}=await params;return <DocumentDetailPage id={id}/>;}
