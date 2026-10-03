BEGIN;
--
-- Add field gateway_order_id to healthcarepayment
--
ALTER TABLE "rcm_healthcare_payments" ADD COLUMN "gateway_order_id" varchar(128) DEFAULT '' NOT NULL;
ALTER TABLE "rcm_healthcare_payments" ALTER COLUMN "gateway_order_id" DROP DEFAULT;
--
-- Add field gateway_payment_id to healthcarepayment
--
ALTER TABLE "rcm_healthcare_payments" ADD COLUMN "gateway_payment_id" varchar(128) DEFAULT '' NOT NULL;
ALTER TABLE "rcm_healthcare_payments" ALTER COLUMN "gateway_payment_id" DROP DEFAULT;
--
-- Create model PatientBillingAccount
--
CREATE TABLE "billing_patient_accounts" ("is_active" boolean NOT NULL, "is_deleted" boolean NOT NULL, "deleted_at" timestamp with time zone NULL, "deleted_by_id" uuid NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "id" uuid NOT NULL PRIMARY KEY, "account_number" varchar(50) NOT NULL, "status" varchar(20) NOT NULL, "currency" varchar(3) NOT NULL, "opening_balance" numeric(14, 2) NOT NULL, "credit_limit" numeric(14, 2) NOT NULL, "current_balance" numeric(14, 2) NOT NULL, "notes" text NOT NULL, "organization_id" uuid NOT NULL, "patient_id" uuid NOT NULL UNIQUE);
--
-- Create model PatientBillingStatement
--
CREATE TABLE "billing_patient_statements" ("is_active" boolean NOT NULL, "is_deleted" boolean NOT NULL, "deleted_at" timestamp with time zone NULL, "deleted_by_id" uuid NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "id" uuid NOT NULL PRIMARY KEY, "statement_number" varchar(60) NOT NULL, "period_start" date NOT NULL, "period_end" date NOT NULL, "opening_balance" numeric(14, 2) NOT NULL, "charges" numeric(14, 2) NOT NULL, "payments" numeric(14, 2) NOT NULL, "adjustments" numeric(14, 2) NOT NULL, "closing_balance" numeric(14, 2) NOT NULL, "status" varchar(20) NOT NULL, "issued_at" timestamp with time zone NULL, "account_id" uuid NOT NULL);
--
-- Create model PatientGuarantor
--
CREATE TABLE "billing_patient_guarantors" ("is_active" boolean NOT NULL, "is_deleted" boolean NOT NULL, "deleted_at" timestamp with time zone NULL, "deleted_by_id" uuid NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "id" uuid NOT NULL PRIMARY KEY, "name" varchar(255) NOT NULL, "relationship" varchar(100) NOT NULL, "phone" varchar(30) NOT NULL, "email" varchar(254) NOT NULL, "address" jsonb NOT NULL, "is_primary" boolean NOT NULL, "organization_id" uuid NOT NULL, "patient_id" uuid NOT NULL);
--
-- Create model PatientFinancialResponsibility
--
CREATE TABLE "billing_patient_responsibilities" ("is_active" boolean NOT NULL, "is_deleted" boolean NOT NULL, "deleted_at" timestamp with time zone NULL, "deleted_by_id" uuid NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "id" uuid NOT NULL PRIMARY KEY, "party_type" varchar(20) NOT NULL, "percentage" numeric(5, 2) NOT NULL, "priority" integer NOT NULL CHECK ("priority" >= 0), "effective_from" date NOT NULL, "effective_to" date NULL, "notes" text NOT NULL, "account_id" uuid NOT NULL, "guarantor_id" uuid NULL);
--
-- Create index pba_org_status_idx on field(s) organization, status of model patientbillingaccount
--
CREATE INDEX "pba_org_status_idx" ON "billing_patient_accounts" ("organization_id", "status");
--
-- Create index pba_org_patient_idx on field(s) organization, patient of model patientbillingaccount
--
CREATE INDEX "pba_org_patient_idx" ON "billing_patient_accounts" ("organization_id", "patient_id");
--
-- Create constraint unique_patient_billing_account_number on model patientbillingaccount
--
ALTER TABLE "billing_patient_accounts" ADD CONSTRAINT "unique_patient_billing_account_number" UNIQUE ("organization_id", "account_number");
--
-- Create constraint unique_patient_billing_account_patient on model patientbillingaccount
--
ALTER TABLE "billing_patient_accounts" ADD CONSTRAINT "unique_patient_billing_account_patient" UNIQUE ("organization_id", "patient_id");
--
-- Create constraint patient_billing_opening_balance_nonnegative on model patientbillingaccount
--
ALTER TABLE "billing_patient_accounts" ADD CONSTRAINT "patient_billing_opening_balance_nonnegative" CHECK ("opening_balance" >= 0.00);
--
-- Create index pstmt_account_end_idx on field(s) account, period_end of model patientbillingstatement
--
CREATE INDEX "pstmt_account_end_idx" ON "billing_patient_statements" ("account_id", "period_end");
--
-- Create index pstmt_account_status_idx on field(s) account, status of model patientbillingstatement
--
CREATE INDEX "pstmt_account_status_idx" ON "billing_patient_statements" ("account_id", "status");
--
-- Create constraint unique_patient_statement_number on model patientbillingstatement
--
ALTER TABLE "billing_patient_statements" ADD CONSTRAINT "unique_patient_statement_number" UNIQUE ("account_id", "statement_number");
--
-- Create constraint unique_patient_statement_period on model patientbillingstatement
--
ALTER TABLE "billing_patient_statements" ADD CONSTRAINT "unique_patient_statement_period" UNIQUE ("account_id", "period_start", "period_end");
--
-- Create constraint patient_statement_valid_period on model patientbillingstatement
--
ALTER TABLE "billing_patient_statements" ADD CONSTRAINT "patient_statement_valid_period" CHECK ("period_end" >= ("period_start"));
--
-- Create index pguarantor_org_patient_idx on field(s) organization, patient of model patientguarantor
--
CREATE INDEX "pguarantor_org_patient_idx" ON "billing_patient_guarantors" ("organization_id", "patient_id");
--
-- Create index pguarantor_patient_primary_idx on field(s) patient, is_primary of model patientguarantor
--
CREATE INDEX "pguarantor_patient_primary_idx" ON "billing_patient_guarantors" ("patient_id", "is_primary");
--
-- Create index presp_account_party_idx on field(s) account, party_type of model patientfinancialresponsibility
--
CREATE INDEX "presp_account_party_idx" ON "billing_patient_responsibilities" ("account_id", "party_type");
--
-- Create index presp_account_date_idx on field(s) account, effective_from of model patientfinancialresponsibility
--
CREATE INDEX "presp_account_date_idx" ON "billing_patient_responsibilities" ("account_id", "effective_from");
CREATE INDEX "rcm_healthcare_payments_gateway_order_id_50d26e12" ON "rcm_healthcare_payments" ("gateway_order_id");
CREATE INDEX "rcm_healthcare_payments_gateway_order_id_50d26e12_like" ON "rcm_healthcare_payments" ("gateway_order_id" varchar_pattern_ops);
CREATE INDEX "rcm_healthcare_payments_gateway_payment_id_7929cace" ON "rcm_healthcare_payments" ("gateway_payment_id");
CREATE INDEX "rcm_healthcare_payments_gateway_payment_id_7929cace_like" ON "rcm_healthcare_payments" ("gateway_payment_id" varchar_pattern_ops);
ALTER TABLE "billing_patient_accounts" ADD CONSTRAINT "billing_patient_acco_organization_id_5ae36998_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "billing_patient_accounts" ADD CONSTRAINT "billing_patient_accounts_patient_id_6463b055_fk_patients_id" FOREIGN KEY ("patient_id") REFERENCES "patients" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "billing_patient_accounts_is_active_fdb31c7f" ON "billing_patient_accounts" ("is_active");
CREATE INDEX "billing_patient_accounts_is_deleted_6c6cb3e5" ON "billing_patient_accounts" ("is_deleted");
CREATE INDEX "billing_patient_accounts_created_at_060d2ad3" ON "billing_patient_accounts" ("created_at");
CREATE INDEX "billing_patient_accounts_updated_at_f74f4b6b" ON "billing_patient_accounts" ("updated_at");
CREATE INDEX "billing_patient_accounts_account_number_873cd8ce" ON "billing_patient_accounts" ("account_number");
CREATE INDEX "billing_patient_accounts_account_number_873cd8ce_like" ON "billing_patient_accounts" ("account_number" varchar_pattern_ops);
CREATE INDEX "billing_patient_accounts_status_e0ec1d7a" ON "billing_patient_accounts" ("status");
CREATE INDEX "billing_patient_accounts_status_e0ec1d7a_like" ON "billing_patient_accounts" ("status" varchar_pattern_ops);
CREATE INDEX "billing_patient_accounts_organization_id_5ae36998" ON "billing_patient_accounts" ("organization_id");
ALTER TABLE "billing_patient_statements" ADD CONSTRAINT "billing_patient_stat_account_id_06f4bf29_fk_billing_p" FOREIGN KEY ("account_id") REFERENCES "billing_patient_accounts" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "billing_patient_statements_is_active_6805a927" ON "billing_patient_statements" ("is_active");
CREATE INDEX "billing_patient_statements_is_deleted_1b18dde2" ON "billing_patient_statements" ("is_deleted");
CREATE INDEX "billing_patient_statements_created_at_bdc1ba32" ON "billing_patient_statements" ("created_at");
CREATE INDEX "billing_patient_statements_updated_at_fdb7ec92" ON "billing_patient_statements" ("updated_at");
CREATE INDEX "billing_patient_statements_statement_number_d8bbffba" ON "billing_patient_statements" ("statement_number");
CREATE INDEX "billing_patient_statements_statement_number_d8bbffba_like" ON "billing_patient_statements" ("statement_number" varchar_pattern_ops);
CREATE INDEX "billing_patient_statements_status_cd53c8fc" ON "billing_patient_statements" ("status");
CREATE INDEX "billing_patient_statements_status_cd53c8fc_like" ON "billing_patient_statements" ("status" varchar_pattern_ops);
CREATE INDEX "billing_patient_statements_account_id_06f4bf29" ON "billing_patient_statements" ("account_id");
ALTER TABLE "billing_patient_guarantors" ADD CONSTRAINT "billing_patient_guar_organization_id_ae6bd8cf_fk_organizat" FOREIGN KEY ("organization_id") REFERENCES "organizations" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "billing_patient_guarantors" ADD CONSTRAINT "billing_patient_guarantors_patient_id_8daf0c5a_fk_patients_id" FOREIGN KEY ("patient_id") REFERENCES "patients" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "billing_patient_guarantors_is_active_35bf9961" ON "billing_patient_guarantors" ("is_active");
CREATE INDEX "billing_patient_guarantors_is_deleted_0bb0cf62" ON "billing_patient_guarantors" ("is_deleted");
CREATE INDEX "billing_patient_guarantors_created_at_73f832cc" ON "billing_patient_guarantors" ("created_at");
CREATE INDEX "billing_patient_guarantors_updated_at_7c40d965" ON "billing_patient_guarantors" ("updated_at");
CREATE INDEX "billing_patient_guarantors_is_primary_d155c1c3" ON "billing_patient_guarantors" ("is_primary");
CREATE INDEX "billing_patient_guarantors_organization_id_ae6bd8cf" ON "billing_patient_guarantors" ("organization_id");
CREATE INDEX "billing_patient_guarantors_patient_id_8daf0c5a" ON "billing_patient_guarantors" ("patient_id");
ALTER TABLE "billing_patient_responsibilities" ADD CONSTRAINT "billing_patient_resp_account_id_68c887fc_fk_billing_p" FOREIGN KEY ("account_id") REFERENCES "billing_patient_accounts" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "billing_patient_responsibilities" ADD CONSTRAINT "billing_patient_resp_guarantor_id_fd0f6cda_fk_billing_p" FOREIGN KEY ("guarantor_id") REFERENCES "billing_patient_guarantors" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "billing_patient_responsibilities_is_active_cb864073" ON "billing_patient_responsibilities" ("is_active");
CREATE INDEX "billing_patient_responsibilities_is_deleted_16f3966f" ON "billing_patient_responsibilities" ("is_deleted");
CREATE INDEX "billing_patient_responsibilities_created_at_c69ab40c" ON "billing_patient_responsibilities" ("created_at");
CREATE INDEX "billing_patient_responsibilities_updated_at_e1e58a3e" ON "billing_patient_responsibilities" ("updated_at");
CREATE INDEX "billing_patient_responsibilities_account_id_68c887fc" ON "billing_patient_responsibilities" ("account_id");
CREATE INDEX "billing_patient_responsibilities_guarantor_id_fd0f6cda" ON "billing_patient_responsibilities" ("guarantor_id");
COMMIT;
