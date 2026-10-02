import { useMutation, useQueryClient } from '@tanstack/react-query';
import { documentKeys, documentMutations } from '../api';
export function useDocumentMutations(){
  const qc=useQueryClient();
  const create=useMutation({...documentMutations.create(),onSuccess:()=>qc.invalidateQueries({queryKey:documentKeys.lists()})});
  const upload=useMutation({...documentMutations.upload(),onSuccess:()=>qc.invalidateQueries({queryKey:documentKeys.lists()})});
  const update=useMutation({...documentMutations.update(),onSuccess:(d)=>Promise.all([qc.invalidateQueries({queryKey:documentKeys.lists()}),qc.invalidateQueries({queryKey:documentKeys.detail(d.id)})])});
  const remove=useMutation({...documentMutations.delete(),onSuccess:()=>qc.invalidateQueries({queryKey:documentKeys.lists()})});
  const createVersion=useMutation({...documentMutations.createVersion(),onSuccess:(v)=>Promise.all([qc.invalidateQueries({queryKey:documentKeys.detail(v.documentId)}),qc.invalidateQueries({queryKey:documentKeys.versions(v.documentId)})])});
  return {create,upload,update,remove,createVersion};
}
