BEGIN;
--
-- Create model HealthcareInvoice
--
CREATE TABLE "rcm_healthcare_invoices" ("id" uuid NOT NULL PRIMARY KEY, "invoice_number" varchar(64) NOT NULL, "patient_reference" varchar(128) NOT NULL, "payer_name" varchar(255) NOT NULL, "claim_reference" varchar(128) NOT NULL, "currency" varchar(3) NOT NULL, "status" varchar(32) NOT NULL, "subtotal" numeric(18, 2) NOT NULL, "tax_total" numeric(18, 2) NOT NULL, "discount_total" numeric(18, 2) NOT NULL, "total" numeric(18, 2) NOT NULL, "paid_total" numeric(18, 2) NOT NULL, "adjustment_total" numeric(18, 2) NOT NULL, "balance_due" numeric(18, 2) NOT NULL, "due_date" date NULL, "finalized_at" timestamp with time zone NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "organization_id" uuid NOT NULL);
--
-- Create model HealthcareAdjustment
--
CREATE TABLE "rcm_healthcare_adjustments" ("id" uuid NOT NULL PRIMARY KEY, "amount" numeric(18, 2) NOT NULL, "reason" varchar(32) NOT NULL, "reference" varchar(128) NOT NULL, "created_at" timestamp with time zone NOT NULL, "organization_id" uuid NOT NULL, "invoice_id" uuid NOT NULL);
--
-- Create model HealthcareInvoiceLine
--
CREATE TABLE "rcm_healthcare_invoice_lines" ("id" uuid NOT NULL PRIMARY KEY, "service_code" varchar(64) NOT NULL, "description" varchar(500) NOT NULL, "quantity" numeric(18, 4) NOT NULL, "unit_price" numeric(18, 2) NOT NULL, "discount_amount" numeric(18, 2) NOT NULL, "tax_amount" numeric(18, 2) NOT NULL, "line_total" numeric(18, 2) NOT NULL, "created_at" timestamp with time zone NOT NULL, "invoice_id" uuid NOT NULL);
--
-- Create model HealthcarePayment
--
CREATE TABLE "rcm_healthcare_payments" ("id" uuid NOT NULL PRIMARY KEY, "amount" numeric(18, 2) NOT NULL, "method" varchar(32) NOT NULL, "reference" varchar(128) NOT NULL, "status" varchar(32) NOT NULL, "posted_at" timestamp with time zone NOT NULL, "created_at" timestamp with time zone NOT NULL, "invoice_id" uuid NOT NULL, "organization_id" uuid NOT NULL);
--
-- Create model HealthcarePaymentAllocation
--
CREATE TABLE "rcm_healthcare_payment_allocations" ("id" uuid NOT NULL PRIMARY KEY, "amount" numeric(18, 2) NOT NULL, "created_at" timestamp with time zone NOT NULL, "invoice_id" uuid NOT NULL, "organization_id" uuid NOT NULL, "payment_id" uuid NOT NULL);
--
-- Create model HealthcareRefund
--
CREATE TABLE "rcm_healthcare_refunds" ("id" uuid NOT NULL PRIMARY KEY, "amount" numeric(18, 2) NOT NULL, "reason" varchar(500) NOT NULL, "status" varchar(32) NOT NULL, "created_at" timestamp with time zone NOT NULL, "processed_at" timestamp with time zone NULL, "organization_id" uuid NOT NULL, "payment_id" uuid NOT NULL);
--
-- Create model HealthcareStatement
--
CREATE TABLE "rcm_healthcare_statements" ("id" uuid NOT NULL PRIMARY KEY, "patient_reference" varchar(128) NOT NULL, "period_start" date NOT NULL, "period_end" date NOT NULL, "opening_balance" numeric(18, 2) NOT NULL, "charges" numeric(18, 2) NOT NULL, "payments" numeric(18, 2) NOT NULL, "adjustments" numeric(18, 2) NOT NULL, "closing_balance" numeric(18, 2) NOT NULL, "created_at" timestamp with time zone NOT NULL, "organization_id" uuid NOT NULL);
--
-- Create model HealthcareBillingAuditLog
--
CREATE TABLE "rcm_healthcare_billing_audit_logs" ("id" uuid NOT NULL PRIMARY KEY, "event_type" varchar(128) NOT NULL, "object_type" varchar(128) NOT NULL, "object_id" varchar(128) NOT NULL, "payload" jsonb NOT NULL, "actor_id" varchar(128) NOT NULL, "created_at" timestamp with time zone NOT NULL, "organization_id" uuid NOT NULL);
--
-- Create model HealthcareBillingIdempotencyKey
--
CREATE TABLE "rcm_healthcare_billing_idempotency" ("id" uuid NOT NULL PRIMARY KEY, "workflow" varchar(160) NOT NULL, "key" varchar(160) NOT NULL, "response_object_type" varchar(128) NOT NULL, "response_object_id" varchar(128) NOT NULL, "created_at" timestamp with time zone NOT NULL, "organization_id" uuid NOT NULL, CONSTRAINT "rcm_hc_bill_idem_uniq" UNIQUE ("organization_id", "workflow", "key"));
--
-- Create model HealthcareBillingOutboxEvent
--
CREATE TABLE "rcm_healthcare_billing_outbox" ("id" uuid NOT NULL PRIMARY KEY, "event_id" uuid NOT NULL UNIQUE, "event_type" varchar(128) NOT NULL, "aggregate_type" varchar(128) NOT NULL, "aggregate_id" varchar(128) NOT NULL, "payload" jsonb NOT NULL, "status" varchar(20) NOT NULL, "attempts" integer NOT NULL CHECK ("attempts" >= 0), "available_at" timestamp with time zone NOT NULL, "published_at" timestamp with time zone NULL, "last_error" text NOT NULL, "created_at" timestamp with time zone NOT NULL, "organization_id" uuid NOT NULL);
--
-- Create index rcm_healthc_organiz_531a5d_idx on field(s) organization, status of model healthcareinvoice
--
CREATE INDEX "rcm_healthc_organiz_531a5d_idx" ON "rcm_healthcare_invoices" ("organization_id", "status");
--
-- Create index rcm_healthc_organiz_7adca0_idx on field(s) organization, patient_reference of model healthcareinvoice
--
CREATE INDEX "rcm_healthc_organiz_7adca0_idx" ON "rcm_healthcare_invoices" ("organization_id", "patient_reference");
--
-- Create index rcm_healthc_organiz_eba9a8_idx on field(s) organization, claim_reference of model healthcareinvoice
--
CREATE INDEX "rcm_healthc_organiz_eba9a8_idx" ON "rcm_healthcare_invoices" ("organization_id", "claim_reference");
--
-- Create constraint rcm_hc_invoice_org_number_uniq on model healthcareinvoice
--
ALTER TABLE "rcm_healthcare_invoices" ADD CONSTRAINT "rcm_hc_invoice_org_number_uniq" UNIQUE ("organization_id", "invoice_number");
--
-- Create constraint rcm_hc_payment_org_reference_uniq on model healthcarepayment
--
ALTER TABLE "rcm_healthcare_payments" ADD CONSTRAINT "rcm_hc_payment_org_reference_uniq" UNIQUE ("organization_id", "reference");
--
-- Create index rcm_healthc_organiz_e91999_idx on field(s) organization, patient_reference of model healthcarestatement
--
CREATE INDEX "rcm_healthc_organiz_e91999_idx" ON "rcm_healthcare_statements" ("organization_id", "patient_reference");
ALTER TABLE "rcm_healthcare_invoices" ADD CONSTRAINT "rcm_healthcare_invoi_organization_id_d551ba6d_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcm_healthcare_invoices_organization_id_d551ba6d" ON "rcm_healthcare_invoices" ("organization_id");
ALTER TABLE "rcm_healthcare_adjustments" ADD CONSTRAINT "rcm_healthcare_adjus_organization_id_823da11a_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "rcm_healthcare_adjustments" ADD CONSTRAINT "rcm_healthcare_adjus_invoice_id_5d0e158d_fk_rcm_healt" FOREIGN KEY ("invoice_id") REFERENCES "rcm_healthcare_invoices" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcm_healthcare_adjustments_organization_id_823da11a" ON "rcm_healthcare_adjustments" ("organization_id");
CREATE INDEX "rcm_healthcare_adjustments_invoice_id_5d0e158d" ON "rcm_healthcare_adjustments" ("invoice_id");
ALTER TABLE "rcm_healthcare_invoice_lines" ADD CONSTRAINT "rcm_healthcare_invoi_invoice_id_78d91ab7_fk_rcm_healt" FOREIGN KEY ("invoice_id") REFERENCES "rcm_healthcare_invoices" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcm_healthcare_invoice_lines_invoice_id_78d91ab7" ON "rcm_healthcare_invoice_lines" ("invoice_id");
ALTER TABLE "rcm_healthcare_payments" ADD CONSTRAINT "rcm_healthcare_payme_invoice_id_00d3b9fc_fk_rcm_healt" FOREIGN KEY ("invoice_id") REFERENCES "rcm_healthcare_invoices" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "rcm_healthcare_payments" ADD CONSTRAINT "rcm_healthcare_payme_organization_id_e9b43cf9_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcm_healthcare_payments_invoice_id_00d3b9fc" ON "rcm_healthcare_payments" ("invoice_id");
CREATE INDEX "rcm_healthcare_payments_organization_id_e9b43cf9" ON "rcm_healthcare_payments" ("organization_id");
ALTER TABLE "rcm_healthcare_payment_allocations" ADD CONSTRAINT "rcm_healthcare_payme_invoice_id_39483a5f_fk_rcm_healt" FOREIGN KEY ("invoice_id") REFERENCES "rcm_healthcare_invoices" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "rcm_healthcare_payment_allocations" ADD CONSTRAINT "rcm_healthcare_payme_organization_id_070f749c_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "rcm_healthcare_payment_allocations" ADD CONSTRAINT "rcm_healthcare_payme_payment_id_25eba114_fk_rcm_healt" FOREIGN KEY ("payment_id") REFERENCES "rcm_healthcare_payments" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcm_healthcare_payment_allocations_invoice_id_39483a5f" ON "rcm_healthcare_payment_allocations" ("invoice_id");
CREATE INDEX "rcm_healthcare_payment_allocations_organization_id_070f749c" ON "rcm_healthcare_payment_allocations" ("organization_id");
CREATE INDEX "rcm_healthcare_payment_allocations_payment_id_25eba114" ON "rcm_healthcare_payment_allocations" ("payment_id");
ALTER TABLE "rcm_healthcare_refunds" ADD CONSTRAINT "rcm_healthcare_refun_organization_id_b3aa3e1a_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "rcm_healthcare_refunds" ADD CONSTRAINT "rcm_healthcare_refun_payment_id_80fcafdb_fk_rcm_healt" FOREIGN KEY ("payment_id") REFERENCES "rcm_healthcare_payments" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcm_healthcare_refunds_organization_id_b3aa3e1a" ON "rcm_healthcare_refunds" ("organization_id");
CREATE INDEX "rcm_healthcare_refunds_payment_id_80fcafdb" ON "rcm_healthcare_refunds" ("payment_id");
ALTER TABLE "rcm_healthcare_statements" ADD CONSTRAINT "rcm_healthcare_state_organization_id_fc8df55e_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcm_healthcare_statements_organization_id_fc8df55e" ON "rcm_healthcare_statements" ("organization_id");
ALTER TABLE "rcm_healthcare_billing_audit_logs" ADD CONSTRAINT "rcm_healthcare_billi_organization_id_76b519cf_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcm_healthcare_billing_audit_logs_organization_id_76b519cf" ON "rcm_healthcare_billing_audit_logs" ("organization_id");
CREATE INDEX "rcm_healthc_organiz_c8d511_idx" ON "rcm_healthcare_billing_audit_logs" ("organization_id", "event_type");
CREATE INDEX "rcm_healthc_organiz_3c5e68_idx" ON "rcm_healthcare_billing_audit_logs" ("organization_id", "object_type", "object_id");
ALTER TABLE "rcm_healthcare_billing_idempotency" ADD CONSTRAINT "rcm_healthcare_billi_organization_id_23f3c599_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcm_healthcare_billing_idempotency_organization_id_23f3c599" ON "rcm_healthcare_billing_idempotency" ("organization_id");
ALTER TABLE "rcm_healthcare_billing_outbox" ADD CONSTRAINT "rcm_healthcare_billi_organization_id_21e9fd72_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcm_healthcare_billing_outbox_organization_id_21e9fd72" ON "rcm_healthcare_billing_outbox" ("organization_id");
CREATE INDEX "rcm_healthc_organiz_96661f_idx" ON "rcm_healthcare_billing_outbox" ("organization_id", "status", "available_at");
COMMIT;
