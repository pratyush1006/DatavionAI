from apps.core.workflows import WorkflowContext
def execute_workflow(*,workflow_class,request,tenant,payload,workflow_name):
 context=WorkflowContext.create(tenant_id=tenant.id,actor_id=request.user.id,workflow_name=workflow_name,request_id=getattr(request,"request_id",None),metadata={"organization_id":str(payload.get("organization_id", ""))})
 return workflow_class(payload=payload).execute(context=context)
