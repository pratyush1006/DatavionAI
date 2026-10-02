import { useQuery } from '@tanstack/react-query';
import { documentQueries } from '../api';
export function useDocumentQuery(id:string){ return useQuery(documentQueries.detail(id)); }
export function useDocumentVersionsQuery(id:string){ return useQuery(documentQueries.versions(id)); }
