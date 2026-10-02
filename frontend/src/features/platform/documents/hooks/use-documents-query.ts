import { useQuery } from '@tanstack/react-query';
import { documentQueries } from '../api';
export function useDocumentsQuery(){ return useQuery(documentQueries.all()); }
