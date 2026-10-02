from django.core.exceptions import ValidationError
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pharmacy.api.serializers import (
    DispensingOrderSerializer,
    MedicationBatchSerializer,
    PharmacyProductSerializer,
    PharmacyReturnSerializer,
    PharmacySerializer,
    PurchaseOrderSerializer,
    StockMovementSerializer,
    StockTransferOrderSerializer,
    SupplierSerializer,
)
from apps.pharmacy.models import (
    DispensingOrder,
    MedicationBatch,
    Pharmacy,
    PharmacyProduct,
    PharmacyReturn,
    ProcurementApproval,
    PurchaseOrder,
    StockMovement,
    StockTransferOrder,
    Supplier,
)
from apps.pharmacy.policies.pharmacy import PharmacyPolicy
from apps.pharmacy.selectors.inventory import expiring_batches, low_stock_products
from apps.pharmacy.services.billing import create_dispensing_bill
from apps.pharmacy.services.dispensing import create_dispensing_order, dispense_order
from apps.pharmacy.services.idempotency import execute_idempotent
from apps.pharmacy.services.inventory import receive_stock
from apps.pharmacy.services.pharmacy import create_pharmacy
from apps.pharmacy.services.procurement import (
    decide_purchase_approval,
    request_purchase_approval,
)
from apps.pharmacy.services.purchase import create_purchase_order
from apps.pharmacy.services.returns import create_pharmacy_return
from apps.pharmacy.services.transfers import (
    complete_transfer_order,
    create_transfer_order,
)


def _organization(request, organization_id):
    from django.apps import apps as django_apps

    Organization = django_apps.get_model("organizations", "Organization")
    organization = Organization.objects.filter(pk=organization_id).first()
    if organization is None:
        return None
    user_organization_id = getattr(request.user, "organization_id", None)
    if user_organization_id is not None and str(user_organization_id) != str(
        organization.id
    ):
        return None
    user_tenant_id = getattr(request.user, "tenant_id", None)
    if user_tenant_id is not None and organization.tenant_id != user_tenant_id:
        return None
    return organization


def _scoped_queryset(queryset, request):
    tenant_id = getattr(request.user, "tenant_id", None)
    if tenant_id is not None:
        queryset = queryset.filter(organization__tenant_id=tenant_id)
    return queryset


def _allowed(request, permission, organization):
    if getattr(request.user, "is_superuser", False):
        return True
    return PharmacyPolicy.allowed(
        user=request.user, permission=permission, organization=organization
    )


def _run_idempotent(request, organization, operation, callback):
    key = request.headers.get("Idempotency-Key")
    if not key:
        payload, status_code = callback()
        return Response(payload, status=status_code)
    try:
        payload, status_code, _ = execute_idempotent(
            organization=organization, key=key, operation=operation, callback=callback
        )
    except ValidationError as exc:
        return Response(
            {"detail": str(exc)},
            status=409 if "already in progress" in str(exc) else 400,
        )
    return Response(payload, status=status_code)


def _deny():
    return Response(
        {"detail": "You do not have permission to perform this pharmacy operation."},
        status=403,
    )


def _require_org_permission(request, organization_id, permission):
    organization = _organization(request, organization_id)
    if organization is None:
        return None, Response({"detail": "Organization not found."}, status=404)
    if not _allowed(request, permission, organization):
        return organization, _deny()
    return organization, None


def _paginate(queryset, request, serializer_class):
    try:
        limit = min(max(int(request.query_params.get("limit", 50)), 1), 100)
        offset = max(int(request.query_params.get("offset", 0)), 0)
    except (TypeError, ValueError):
        return Response(
            {"detail": "limit and offset must be valid integers."}, status=400
        )
    total = queryset.count()
    data = serializer_class(queryset[offset : offset + limit], many=True).data
    return Response({"count": total, "limit": limit, "offset": offset, "results": data})


class PharmacyListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        organization_id = request.query_params.get("organization_id")
        if organization_id:
            organization, error = _require_org_permission(
                request, organization_id, "pharmacy.view"
            )
            if error:
                return error
            queryset = Pharmacy.objects.filter(
                organization=organization, is_active=True
            )
        else:
            if not getattr(request.user, "tenant_id", None):
                return _deny()
            queryset = _scoped_queryset(
                Pharmacy.objects.filter(is_active=True), request
            )
        return _paginate(queryset.order_by("code"), request, PharmacySerializer)

    def post(self, request):
        organization, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.manage"
        )
        if error:
            return error
        if not request.data.get("code") or not request.data.get("name"):
            return Response({"detail": "code and name are required."}, status=400)
        pharmacy = create_pharmacy(
            organization=organization,
            data={
                k: request.data.get(k, "")
                for k in ("code", "name", "address", "phone", "email")
            },
            actor=request.user,
        )
        return Response(PharmacySerializer(pharmacy).data, status=201)


class SupplierListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        qs = _scoped_queryset(Supplier.objects.filter(is_active=True), request)
        organization_id = request.query_params.get("organization_id")
        if organization_id:
            org, error = _require_org_permission(
                request, organization_id, "pharmacy.view"
            )
            if error:
                return error
            qs = qs.filter(organization=org)
        elif not getattr(request.user, "tenant_id", None):
            return _deny()
        return _paginate(qs.order_by("code"), request, SupplierSerializer)

    def post(self, request):
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.manage"
        )
        if error:
            return error
        data = request.data.copy()
        data["organization"] = org.id
        serializer = SupplierSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(SupplierSerializer(obj).data, status=201)


class ProductListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        qs = _scoped_queryset(
            PharmacyProduct.objects.filter(is_active=True), request
        ).select_related("medication", "pharmacy")
        organization_id = request.query_params.get("organization_id")
        if organization_id:
            org, error = _require_org_permission(
                request, organization_id, "pharmacy.view"
            )
            if error:
                return error
            qs = qs.filter(organization=org)
        elif not getattr(request.user, "tenant_id", None):
            return _deny()
        if request.query_params.get("pharmacy_id"):
            qs = qs.filter(pharmacy_id=request.query_params["pharmacy_id"])
        return _paginate(qs.order_by("sku"), request, PharmacyProductSerializer)

    def post(self, request):
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.manage"
        )
        if error:
            return error
        pharmacy = Pharmacy.objects.filter(
            pk=request.data.get("pharmacy"), organization=org, is_active=True
        ).first()
        if pharmacy is None:
            return Response({"detail": "Pharmacy not found."}, status=404)
        data = request.data.copy()
        data["organization"] = org.id
        serializer = PharmacyProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(PharmacyProductSerializer(obj).data, status=201)


class BatchListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        organization_id = request.query_params.get("organization_id")
        if not organization_id:
            return Response({"detail": "organization_id is required."}, status=400)
        org, error = _require_org_permission(request, organization_id, "pharmacy.view")
        if error:
            return error
        qs = MedicationBatch.objects.filter(
            product__organization=org, product__is_active=True
        )
        if request.query_params.get("product_id"):
            qs = qs.filter(product_id=request.query_params["product_id"])
        return _paginate(
            qs.select_related("product").order_by("expiry_date"),
            request,
            MedicationBatchSerializer,
        )


class PurchaseOrderListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        qs = _scoped_queryset(PurchaseOrder.objects.all(), request).select_related(
            "pharmacy", "supplier"
        )
        organization_id = request.query_params.get("organization_id")
        if organization_id:
            org, error = _require_org_permission(
                request, organization_id, "pharmacy.view"
            )
            if error:
                return error
            qs = qs.filter(organization=org)
        return _paginate(qs.order_by("-created_at"), request, PurchaseOrderSerializer)

    def post(self, request):
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.purchasing"
        )
        if error:
            return error
        pharmacy = Pharmacy.objects.filter(
            pk=request.data.get("pharmacy"), organization=org
        ).first()
        supplier = Supplier.objects.filter(
            pk=request.data.get("supplier"), organization=org
        ).first()
        if not pharmacy or not supplier:
            return Response(
                {"detail": "Organization, pharmacy or supplier not found."}, status=404
            )
        line_payload = []
        for item in request.data.get("lines", []):
            product = PharmacyProduct.objects.filter(
                pk=item.get("product"),
                organization=org,
                pharmacy=pharmacy,
                is_active=True,
            ).first()
            if not product:
                return Response(
                    {"detail": "Purchase product not found in pharmacy scope."},
                    status=400,
                )
            line_payload.append(
                {
                    "product": product,
                    "quantity_ordered": item.get("quantity_ordered"),
                    "unit_cost": item.get("unit_cost"),
                    "tax_rate": item.get("tax_rate", 0),
                }
            )
        order = create_purchase_order(
            organization=org,
            pharmacy=pharmacy,
            supplier=supplier,
            order_number=request.data.get("order_number"),
            lines=line_payload,
            actor=request.user,
        )
        return Response(PurchaseOrderSerializer(order).data, status=201)


class DispensingOrderListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        qs = _scoped_queryset(DispensingOrder.objects.all(), request).select_related(
            "pharmacy", "prescription"
        )
        organization_id = request.query_params.get("organization_id")
        if organization_id:
            org, error = _require_org_permission(
                request, organization_id, "pharmacy.view"
            )
            if error:
                return error
            qs = qs.filter(organization=org)
        return _paginate(
            qs.prefetch_related("dispensing_lines").order_by("-created_at"),
            request,
            DispensingOrderSerializer,
        )

    def post(self, request):
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.dispense"
        )
        if error:
            return error
        pharmacy = Pharmacy.objects.filter(
            pk=request.data.get("pharmacy"), organization=org, is_active=True
        ).first()
        from django.apps import apps as django_apps

        Prescription = django_apps.get_model("prescriptions", "Prescription")
        prescription = Prescription.objects.filter(
            pk=request.data.get("prescription"), organization=org
        ).first()
        if not pharmacy or not prescription:
            return Response(
                {"detail": "Organization, pharmacy or prescription not found."},
                status=404,
            )
        lines = []
        for item in request.data.get("lines", []):
            product = PharmacyProduct.objects.filter(
                pk=item.get("product"),
                organization=org,
                pharmacy=pharmacy,
                is_active=True,
            ).first()
            batch = (
                MedicationBatch.objects.filter(
                    pk=item.get("batch"), product=product
                ).first()
                if product
                else None
            )
            if not product or not batch:
                return Response(
                    {
                        "detail": "Dispensing product or batch not found in pharmacy scope."
                    },
                    status=400,
                )
            lines.append(
                {
                    "product": product,
                    "batch": batch,
                    "quantity_prescribed": item.get(
                        "quantity_prescribed", item.get("quantity")
                    ),
                    "second_checker_id": item.get("second_checker_id"),
                }
            )
        order = create_dispensing_order(
            organization=org,
            pharmacy=pharmacy,
            prescription=prescription,
            dispense_number=request.data.get("dispense_number"),
            lines=lines,
            pharmacist_id=request.data.get("pharmacist_id"),
        )
        return Response(DispensingOrderSerializer(order).data, status=201)


class PharmacyReturnListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        organization_id = request.query_params.get("organization_id")
        organization, error = _require_org_permission(
            request, organization_id, "pharmacy.view"
        )
        if error:
            return error
        from django.db.models import Q

        qs = PharmacyReturn.objects.filter(
            Q(dispensing_order__organization=organization)
            | Q(purchase_order__organization=organization)
        ).distinct()
        return _paginate(qs.order_by("-created_at"), request, PharmacyReturnSerializer)

    def post(self, request):
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.inventory"
        )
        if error:
            return error
        from django.apps import apps as django_apps

        DispensingOrderModel = django_apps.get_model("pharmacy", "DispensingOrder")
        PurchaseOrderModel = django_apps.get_model("pharmacy", "PurchaseOrder")
        dispensing_order = (
            DispensingOrderModel.objects.filter(
                pk=request.data.get("dispensing_order"), organization=org
            ).first()
            if request.data.get("dispensing_order")
            else None
        )
        purchase_order = (
            PurchaseOrderModel.objects.filter(
                pk=request.data.get("purchase_order"), organization=org
            ).first()
            if request.data.get("purchase_order")
            else None
        )
        lines = []
        for item in request.data.get("lines", []):
            product = PharmacyProduct.objects.filter(
                pk=item.get("product"), organization=org, is_active=True
            ).first()
            batch = (
                MedicationBatch.objects.filter(
                    pk=item.get("batch"), product=product
                ).first()
                if product
                else None
            )
            if not product or not batch:
                return Response(
                    {"detail": "Return product or batch not found."}, status=400
                )
            lines.append(
                {
                    "product": product,
                    "batch": batch,
                    "quantity": item.get("quantity"),
                    "restockable": item.get("restockable", False),
                }
            )
        result = create_pharmacy_return(
            organization=org,
            return_type=request.data.get("return_type"),
            return_number=request.data.get("return_number"),
            reason=request.data.get("reason", ""),
            lines=lines,
            dispensing_order=dispensing_order,
            purchase_order=purchase_order,
            actor_id=request.user,
        )
        return Response(PharmacyReturnSerializer(result).data, status=201)


class PharmacyInventoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        pharmacy_id = request.query_params.get("pharmacy_id")
        if not pharmacy_id:
            return Response({"detail": "pharmacy_id is required."}, status=400)
        pharmacy = _scoped_queryset(
            Pharmacy.objects.filter(pk=pharmacy_id, is_active=True), request
        ).first()
        if pharmacy is None:
            return Response({"detail": "Pharmacy not found."}, status=404)
        if not _allowed(request, "pharmacy.inventory", pharmacy.organization):
            return _deny()
        products = (
            PharmacyProduct.objects.filter(pharmacy=pharmacy, is_active=True)
            .annotate(stock=Sum("batches__quantity_available"))
            .select_related("medication")
        )
        return Response(
            [
                {
                    "product_id": str(item.id),
                    "sku": item.sku,
                    "medication": item.medication.display_name,
                    "stock": str(item.stock or 0),
                    "reorder_level": str(item.reorder_level),
                }
                for item in products
            ]
        )


class PharmacyOperationalSummaryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        organization, error = _require_org_permission(
            request, request.query_params.get("organization_id"), "pharmacy.view"
        )
        if error:
            return error
        pharmacy_id = request.query_params.get("pharmacy_id")
        if not pharmacy_id:
            return Response({"detail": "pharmacy_id is required."}, status=400)
        pharmacy = Pharmacy.objects.filter(
            pk=pharmacy_id, organization=organization, is_active=True
        ).first()
        if not pharmacy:
            return Response({"detail": "Pharmacy not found."}, status=404)
        low = list(
            low_stock_products(pharmacy_id=pharmacy.id).values(
                "id", "sku", "reorder_level"
            )
        )
        expiring = list(
            expiring_batches(pharmacy_id=pharmacy_id, days=30).values(
                "id", "batch_number", "expiry_date", "quantity_available", "product_id"
            )
        )
        return Response(
            {
                "low_stock_count": len(low),
                "expiring_batch_count": len(expiring),
                "low_stock": low,
                "expiring_batches": expiring,
            }
        )


class ReceiveStockAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.inventory"
        )
        if error:
            return error
        batch = MedicationBatch.objects.filter(
            pk=request.data.get("batch"),
            product__organization=org,
            product__is_active=True,
        ).first()
        if batch is None:
            return Response({"detail": "Batch not found."}, status=404)

        def operation():
            movement = receive_stock(
                organization=org,
                batch=batch,
                quantity=request.data.get("quantity"),
                actor=request.user,
                reference_type=request.data.get("reference_type", "API"),
                reference_id=request.data.get("reference_id"),
                note=request.data.get("note", ""),
            )
            return {
                "movement_id": str(movement.id),
                "batch_id": str(batch.id),
                "quantity": str(movement.quantity),
            }, 201

        return _run_idempotent(request, org, "inventory.receive", operation)


class StockMovementListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        org, error = _require_org_permission(
            request, request.query_params.get("organization_id"), "pharmacy.inventory"
        )
        if error:
            return error
        queryset = StockMovement.objects.filter(organization=org).select_related(
            "batch__product__medication"
        )
        return _paginate(
            queryset.order_by("-created_at"), request, StockMovementSerializer
        )


class StockTransferListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        org, error = _require_org_permission(
            request, request.query_params.get("organization_id"), "pharmacy.inventory"
        )
        if error:
            return error
        queryset = (
            StockTransferOrder.objects.filter(organization=org)
            .select_related("source_pharmacy", "destination_pharmacy")
            .prefetch_related("lines")
        )
        return _paginate(
            queryset.order_by("-created_at"), request, StockTransferOrderSerializer
        )

    def post(self, request):
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.inventory"
        )
        if error:
            return error
        source = Pharmacy.objects.filter(
            pk=request.data.get("source_pharmacy"), organization=org
        ).first()
        destination = Pharmacy.objects.filter(
            pk=request.data.get("destination_pharmacy"), organization=org
        ).first()
        if not source or not destination:
            return Response(
                {"detail": "Source or destination warehouse not found."}, status=404
            )
        lines = []
        for item in request.data.get("lines", []):
            batch = (
                MedicationBatch.objects.select_related("product")
                .filter(pk=item.get("source_batch"), product__organization=org)
                .first()
            )
            product = PharmacyProduct.objects.filter(
                pk=item.get("destination_product"), organization=org
            ).first()
            if not batch or not product:
                return Response(
                    {"detail": "Transfer product or batch not found."}, status=400
                )
            lines.append(
                {
                    "source_batch": batch,
                    "destination_product": product,
                    "quantity": item.get("quantity"),
                }
            )
        try:
            transfer = create_transfer_order(
                organization=org,
                source_pharmacy=source,
                destination_pharmacy=destination,
                transfer_number=request.data.get("transfer_number"),
                lines=lines,
                actor_id=request.user.id,
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
        return Response(StockTransferOrderSerializer(transfer).data, status=201)


class CompleteStockTransferAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, transfer_id):
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.inventory"
        )
        if error:
            return error
        transfer = StockTransferOrder.objects.filter(
            pk=transfer_id, organization=org
        ).first()
        if not transfer:
            return Response({"detail": "Transfer not found."}, status=404)
        try:
            transfer = complete_transfer_order(
                organization=org, order=transfer, actor_id=request.user
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
        return Response(StockTransferOrderSerializer(transfer).data)


class DispenseOrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, order_id):
        order = DispensingOrder.objects.filter(pk=order_id).first()
        if order is None:
            return Response({"detail": "Dispensing order not found."}, status=404)
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.dispense"
        )
        if error:
            return error
        if order.organization_id != org.id:
            return Response(
                {"detail": "Dispensing order is outside the organization scope."},
                status=403,
            )
        requested = []
        for item in request.data.get("lines", []):
            product = PharmacyProduct.objects.filter(
                pk=item.get("product"),
                organization=org,
                pharmacy_id=order.pharmacy_id,
                is_active=True,
            ).first()
            batch = (
                MedicationBatch.objects.filter(
                    pk=item.get("batch"), product=product
                ).first()
                if product
                else None
            )
            if not product or not batch:
                return Response(
                    {"detail": "Dispensing product or batch not found."}, status=400
                )
            requested.append(
                {
                    "product": product,
                    "batch": batch,
                    "quantity": item.get("quantity"),
                    "second_checker_id": item.get("second_checker_id"),
                }
            )
        try:
            result = dispense_order(
                organization=org,
                order=order,
                requested_lines=requested,
                pharmacist_id=request.data.get("pharmacist_id", request.user.id),
            )
        except (ValidationError, ValueError) as exc:
            return Response({"detail": str(exc)}, status=400)
        payload = DispensingOrderSerializer(result).data
        return _run_idempotent(
            request, org, "dispensing.dispense", lambda: (payload, 200)
        )


class PurchaseApprovalRequestAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, order_id):
        order = PurchaseOrder.objects.filter(pk=order_id).first()
        if order is None:
            return Response({"detail": "Purchase order not found."}, status=404)
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.purchasing"
        )
        if error:
            return error
        if order.organization_id != org.id:
            return Response(
                {"detail": "Purchase order is outside the organization scope."},
                status=403,
            )

        def operation():
            approval = request_purchase_approval(
                organization=org, purchase_order=order, actor_id=request.user
            )
            return {"approval_id": str(approval.id), "status": approval.status}, 201

        return _run_idempotent(request, org, "purchasing.request_approval", operation)


class PurchaseApprovalDecisionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, approval_id):
        approval = ProcurementApproval.objects.filter(pk=approval_id).first()
        if approval is None:
            return Response({"detail": "Approval not found."}, status=404)
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.purchasing.approve"
        )
        if error:
            return error
        if approval.organization_id != org.id:
            return Response(
                {"detail": "Approval is outside the organization scope."}, status=403
            )
        approved = bool(request.data.get("approved"))
        reason = request.data.get("reason", "")
        try:
            result = decide_purchase_approval(
                organization=org,
                approval=approval,
                approved=approved,
                actor_id=request.user,
                reason=reason,
            )
        except ValidationError as exc:
            return Response({"detail": str(exc)}, status=400)
        payload = {
            "approval_id": str(result.id),
            "status": result.status,
            "purchase_order_status": result.purchase_order.status,
        }
        return _run_idempotent(
            request, org, "purchasing.decide_approval", lambda: (payload, 200)
        )


class DispensingBillAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, order_id):
        order = DispensingOrder.objects.filter(pk=order_id).first()
        if order is None:
            return Response({"detail": "Dispensing order not found."}, status=404)
        org, error = _require_org_permission(
            request, request.data.get("organization_id"), "pharmacy.view"
        )
        if error:
            return error
        if order.organization_id != org.id:
            return Response(
                {"detail": "Dispensing order is outside the organization scope."},
                status=403,
            )

        def operation():
            bill, created = create_dispensing_bill(
                organization=org, dispensing_order=order, actor_id=request.user
            )
            return {
                "billing_id": str(bill.id),
                "created": created,
                "subtotal": str(bill.subtotal),
                "tax_amount": str(bill.tax_amount),
                "total_amount": str(bill.total_amount),
                "status": bill.status,
            }, (201 if created else 200)

        return _run_idempotent(request, org, "billing.dispensing_bill", operation)
