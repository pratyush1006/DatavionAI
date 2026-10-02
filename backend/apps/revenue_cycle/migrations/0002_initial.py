import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('patient_core', '0001_initial'),
        ('revenue_cycle', '0001_initial'),
        ('revenue_cycle_billing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentposting',
            name='invoice',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='revenue_cycle_payment_postings',
                to='revenue_cycle_billing.healthcareinvoice',
            ),
        ),
        migrations.AddField(
            model_name='paymentposting',
            name='organization',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='revenue_cycle_payment_postings',
                to='organizations.organization',
            ),
        ),
        migrations.AddField(
            model_name='paymentposting',
            name='patient',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='revenue_cycle_payment_postings',
                to='patient_core.patient',
            ),
        ),
        migrations.AddField(
            model_name='paymentposting',
            name='posted_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='revenue_cycle_payment_postings',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='priorauthorization',
            name='approved_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='revenue_cycle_prior_authorizations_approved',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='priorauthorization',
            name='organization',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='revenue_cycle_prior_authorizations',
                to='organizations.organization',
            ),
        ),
        migrations.AddField(
            model_name='priorauthorization',
            name='patient',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='revenue_cycle_prior_authorizations',
                to='patient_core.patient',
            ),
        ),
        migrations.AddField(
            model_name='revenuecycleintegrationrecord',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='revenue_cycle_integration_records',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='revenuecycleintegrationrecord',
            name='organization',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='revenue_cycle_integration_records',
                to='organizations.organization',
            ),
        ),
        migrations.AddField(
            model_name='revenuemetricsnapshot',
            name='organization',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='revenue_cycle_metric_snapshots',
                to='organizations.organization',
            ),
        ),
        migrations.AddField(
            model_name='scrubrule',
            name='organization',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='revenue_cycle_scrub_rules',
                to='organizations.organization',
            ),
        ),
        migrations.AddField(
            model_name='claimscrubfinding',
            name='rule',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='findings',
                to='revenue_cycle.scrubrule',
            ),
        ),
        migrations.AddIndex(
            model_name='appeal',
            index=models.Index(
                fields=['organization', 'status'], name='rc_appeal_org_status_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='appeal',
            index=models.Index(
                fields=['organization', 'claim_reference'],
                name='rc_appeal_org_claim_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='appeal',
            index=models.Index(
                fields=['organization', 'patient'], name='rc_appeal_org_patient_idx'
            ),
        ),
        migrations.AddConstraint(
            model_name='appeal',
            constraint=models.UniqueConstraint(
                fields=('organization', 'appeal_number'),
                name='rc_appeal_org_number_unique',
            ),
        ),
        migrations.AddConstraint(
            model_name='appeal',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='rc_appeal_org_idempotency_unique',
            ),
        ),
        migrations.AddConstraint(
            model_name='appeal',
            constraint=models.CheckConstraint(
                condition=models.Q(('requested_amount__gte', 0)),
                name='rc_appeal_requested_nonnegative',
            ),
        ),
        migrations.AddConstraint(
            model_name='appeal',
            constraint=models.CheckConstraint(
                condition=models.Q(('approved_amount__gte', 0)),
                name='rc_appeal_approved_nonnegative',
            ),
        ),
        migrations.AddConstraint(
            model_name='appeal',
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ('approved_amount__lte', models.F('requested_amount'))
                ),
                name='rc_appeal_approved_lte_requested',
            ),
        ),
        migrations.AddIndex(
            model_name='araccount',
            index=models.Index(
                fields=['organization', 'patient', 'status'],
                name='rc_ar_org_patient_status_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='araccount',
            index=models.Index(
                fields=['organization', 'balance_amount'], name='rc_ar_org_balance_idx'
            ),
        ),
        migrations.AddConstraint(
            model_name='araccount',
            constraint=models.UniqueConstraint(
                fields=('organization', 'account_number'),
                name='unique_rc_ar_account_number',
            ),
        ),
        migrations.AddConstraint(
            model_name='araccount',
            constraint=models.CheckConstraint(
                condition=models.Q(('balance_amount__gte', 0)),
                name='rc_ar_balance_non_negative',
            ),
        ),
        migrations.AddConstraint(
            model_name='araccount',
            constraint=models.CheckConstraint(
                condition=models.Q(('total_charges__gte', 0)),
                name='rc_ar_charges_non_negative',
            ),
        ),
        migrations.AddConstraint(
            model_name='araccount',
            constraint=models.CheckConstraint(
                condition=models.Q(('total_payments__gte', 0)),
                name='rc_ar_payments_non_negative',
            ),
        ),
        migrations.AddConstraint(
            model_name='araccount',
            constraint=models.CheckConstraint(
                condition=models.Q(('total_adjustments__gte', 0)),
                name='rc_ar_adjustments_non_negative',
            ),
        ),
        migrations.AddConstraint(
            model_name='araccount',
            constraint=models.CheckConstraint(
                condition=models.Q(('total_write_offs__gte', 0)),
                name='rc_ar_writeoffs_non_negative',
            ),
        ),
        migrations.AddIndex(
            model_name='aractivitylog',
            index=models.Index(
                fields=['organization', 'account', 'performed_at'],
                name='rc_ar_activity_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='artransaction',
            index=models.Index(
                fields=['organization', 'account', 'transaction_date'],
                name='rc_ar_account_date_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='artransaction',
            index=models.Index(
                fields=['organization', 'patient', 'transaction_date'],
                name='rc_ar_patient_date_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='artransaction',
            index=models.Index(
                fields=['organization', 'transaction_type', 'status'],
                name='rc_ar_type_status_idx',
            ),
        ),
        migrations.AddConstraint(
            model_name='artransaction',
            constraint=models.UniqueConstraint(
                fields=('organization', 'transaction_number'),
                name='unique_rc_ar_transaction_number',
            ),
        ),
        migrations.AddConstraint(
            model_name='artransaction',
            constraint=models.CheckConstraint(
                condition=models.Q(('amount__gt', 0)),
                name='rc_ar_transaction_amount_positive',
            ),
        ),
        migrations.AddIndex(
            model_name='charge',
            index=models.Index(
                fields=['tenant_id', 'organization', 'patient'],
                name='rc_cc_charge_scope_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='charge',
            index=models.Index(
                fields=['tenant_id', 'status'], name='rc_cc_charge_status_idx'
            ),
        ),
        migrations.AddConstraint(
            model_name='charge',
            constraint=models.CheckConstraint(
                condition=models.Q(('quantity__gt', 0)),
                name='rc_cc_charge_quantity_gt_zero',
            ),
        ),
        migrations.AddConstraint(
            model_name='charge',
            constraint=models.CheckConstraint(
                condition=models.Q(('unit_price__gte', 0)),
                name='rc_cc_charge_unit_price_gte_zero',
            ),
        ),
        migrations.AddConstraint(
            model_name='charge',
            constraint=models.CheckConstraint(
                condition=models.Q(('total_amount__gte', 0)),
                name='rc_cc_charge_total_gte_zero',
            ),
        ),
        migrations.AddIndex(
            model_name='claimscrub',
            index=models.Index(
                fields=['organization', 'claim_reference', 'status'],
                name='rc_claim_scrub_org_claim_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='claimscrub',
            index=models.Index(
                fields=['organization', 'patient', 'created_at'],
                name='rc_claim_scrub_org_patient_idx',
            ),
        ),
        migrations.AddConstraint(
            model_name='claimscrub',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='rc_claim_scrub_org_idempotency_uniq',
            ),
        ),
        migrations.AddIndex(
            model_name='claimsubmission',
            index=models.Index(
                fields=['organization', 'status'], name='rc_claim_sub_org_status_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='claimsubmission',
            index=models.Index(
                fields=['organization', 'patient'], name='rc_claim_sub_org_patient_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='claimsubmission',
            index=models.Index(
                fields=['organization', 'payer_id'], name='rc_claim_sub_org_payer_idx'
            ),
        ),
        migrations.AddConstraint(
            model_name='claimsubmission',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='rc_claim_submission_org_idempotency_uniq',
            ),
        ),
        migrations.AddConstraint(
            model_name='claimsubmission',
            constraint=models.UniqueConstraint(
                fields=('organization', 'claim_reference'),
                name='rc_claim_submission_org_reference_uniq',
            ),
        ),
        migrations.AddIndex(
            model_name='codingrecord',
            index=models.Index(
                fields=['organization', 'patient', 'service_date'],
                name='rc_coding_org_patient_date_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='codingrecord',
            index=models.Index(
                fields=['organization', 'status', 'service_date'],
                name='rc_coding_org_status_date_idx',
            ),
        ),
        migrations.AddConstraint(
            model_name='codingrecord',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='rc_coding_org_idempotency_uniq',
            ),
        ),
        migrations.AddConstraint(
            model_name='codingrecord',
            constraint=models.UniqueConstraint(
                condition=models.Q(('is_deleted', False)),
                fields=('organization', 'source_reference'),
                name='rc_coding_org_source_active_uniq',
            ),
        ),
        migrations.AddIndex(
            model_name='codeassignment',
            index=models.Index(
                fields=['coding_record', 'code_system', 'code'],
                name='rc_code_record_system_code_idx',
            ),
        ),
        migrations.AddConstraint(
            model_name='codeassignment',
            constraint=models.UniqueConstraint(
                fields=('coding_record', 'code_system', 'code', 'sequence'),
                name='rc_code_record_code_sequence_uniq',
            ),
        ),
        migrations.AddIndex(
            model_name='denial',
            index=models.Index(
                fields=['organization', 'status'], name='revenue_cyc_organiz_807e04_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='denial',
            index=models.Index(
                fields=['organization', 'patient', 'received_at'],
                name='revenue_cyc_organiz_95bd03_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='denial',
            index=models.Index(
                fields=['organization', 'denial_code'],
                name='revenue_cyc_organiz_614319_idx',
            ),
        ),
        migrations.AddConstraint(
            model_name='denial',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='rc_denial_org_idempotency_uniq',
            ),
        ),
        migrations.AddIndex(
            model_name='eligibility',
            index=models.Index(
                fields=['organization', 'patient', '-requested_at'],
                name='rc_elig_patient_req_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='eligibility',
            index=models.Index(
                fields=['organization', 'status'], name='rc_elig_org_status_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='eligibility',
            index=models.Index(
                fields=['organization', 'payer_id', 'member_id'],
                name='rc_elig_org_payer_member_idx',
            ),
        ),
        migrations.AddConstraint(
            model_name='eligibility',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='rc_elig_org_idempotency_uniq',
            ),
        ),
        migrations.AddIndex(
            model_name='era',
            index=models.Index(
                fields=['organization', 'status'], name='rc_era_org_status_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='era',
            index=models.Index(
                fields=['organization', 'patient'], name='rc_era_org_patient_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='era',
            index=models.Index(
                fields=['organization', 'received_at'], name='rc_era_org_received_idx'
            ),
        ),
        migrations.AddConstraint(
            model_name='era',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='rc_era_org_idempotency_uniq',
            ),
        ),
        migrations.AddConstraint(
            model_name='era',
            constraint=models.UniqueConstraint(
                fields=('organization', 'trace_number'), name='rc_era_org_trace_uniq'
            ),
        ),
        migrations.AddConstraint(
            model_name='era',
            constraint=models.CheckConstraint(
                condition=models.Q(('payment_amount__gte', 0)),
                name='rc_era_payment_nonnegative',
            ),
        ),
        migrations.AddConstraint(
            model_name='era',
            constraint=models.CheckConstraint(
                condition=models.Q(('adjustment_amount__gte', 0)),
                name='rc_era_adjustment_nonnegative',
            ),
        ),
        migrations.AddIndex(
            model_name='insuranceverification',
            index=models.Index(
                fields=['organization', 'patient', '-requested_at'],
                name='rc_iv_org_patient_req_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='insuranceverification',
            index=models.Index(
                fields=['organization', 'status'], name='rc_iv_org_status_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='insuranceverification',
            index=models.Index(
                fields=['organization', 'payer_id', 'member_id'],
                name='rc_iv_org_payer_member_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='insuranceverification',
            index=models.Index(
                fields=['organization', 'outcome'], name='rc_iv_org_outcome_idx'
            ),
        ),
        migrations.AddConstraint(
            model_name='insuranceverification',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='rc_iv_org_idempotency_uniq',
            ),
        ),
        migrations.AddIndex(
            model_name='paymentposting',
            index=models.Index(
                fields=['organization', 'status'], name='rc_pp_org_status_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='paymentposting',
            index=models.Index(
                fields=['organization', 'patient'], name='rc_pp_org_patient_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='paymentposting',
            index=models.Index(
                fields=['organization', 'posted_at'], name='rc_pp_org_posted_idx'
            ),
        ),
        migrations.AddConstraint(
            model_name='paymentposting',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='rc_pp_org_idempotency_uniq',
            ),
        ),
        migrations.AddConstraint(
            model_name='paymentposting',
            constraint=models.CheckConstraint(
                condition=models.Q(('amount__gt', 0)), name='rc_pp_amount_positive'
            ),
        ),
        migrations.AddConstraint(
            model_name='paymentposting',
            constraint=models.CheckConstraint(
                condition=models.Q(('adjustment_amount__gte', 0)),
                name='rc_pp_adjustment_nonnegative',
            ),
        ),
        migrations.AddIndex(
            model_name='priorauthorization',
            index=models.Index(
                fields=['organization', 'patient', '-requested_at'],
                name='rc_pa_org_patient_req_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='priorauthorization',
            index=models.Index(
                fields=['organization', 'status'], name='rc_pa_org_status_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='priorauthorization',
            index=models.Index(
                fields=['organization', 'payer_id', 'member_id'],
                name='rc_pa_org_payer_member_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='priorauthorization',
            index=models.Index(
                fields=['organization', 'procedure_code', 'requested_service_date'],
                name='rc_pa_org_proc_date_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='priorauthorization',
            index=models.Index(
                fields=['organization', 'outcome'], name='rc_pa_org_outcome_idx'
            ),
        ),
        migrations.AddConstraint(
            model_name='priorauthorization',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='rc_pa_org_idempotency_uniq',
            ),
        ),
        migrations.AddIndex(
            model_name='revenuecycleintegrationrecord',
            index=models.Index(
                fields=['organization', 'status', 'created_at'],
                name='rc_integration_status_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='revenuecycleintegrationrecord',
            index=models.Index(
                fields=['organization', 'source', 'created_at'],
                name='rc_integration_source_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='revenuecycleintegrationrecord',
            index=models.Index(
                fields=['organization', 'aggregate_id'],
                name='rc_integration_aggregate_idx',
            ),
        ),
        migrations.AddConstraint(
            model_name='revenuecycleintegrationrecord',
            constraint=models.UniqueConstraint(
                fields=('organization', 'idempotency_key'),
                name='unique_rc_integration_idempotency',
            ),
        ),
        migrations.AddConstraint(
            model_name='revenuecycleintegrationrecord',
            constraint=models.CheckConstraint(
                condition=models.Q(('attempts__gte', 0)),
                name='rc_integration_attempts_non_negative',
            ),
        ),
        migrations.AddIndex(
            model_name='revenuemetricsnapshot',
            index=models.Index(
                fields=['organization', 'period_end'], name='rc_metric_org_period_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='revenuemetricsnapshot',
            index=models.Index(
                fields=['organization', 'period'], name='rc_metric_org_type_idx'
            ),
        ),
        migrations.AddConstraint(
            model_name='revenuemetricsnapshot',
            constraint=models.UniqueConstraint(
                fields=('organization', 'period', 'period_start', 'period_end'),
                name='unique_rc_metric_snapshot_period',
            ),
        ),
        migrations.AddConstraint(
            model_name='revenuemetricsnapshot',
            constraint=models.CheckConstraint(
                condition=models.Q(('period_end__gte', models.F('period_start'))),
                name='rc_metric_valid_period',
            ),
        ),
        migrations.AddConstraint(
            model_name='revenuemetricsnapshot',
            constraint=models.CheckConstraint(
                condition=models.Q(('gross_charges__gte', 0)),
                name='rc_metric_charges_non_negative',
            ),
        ),
        migrations.AddConstraint(
            model_name='revenuemetricsnapshot',
            constraint=models.CheckConstraint(
                condition=models.Q(('payments__gte', 0)),
                name='rc_metric_payments_non_negative',
            ),
        ),
        migrations.AddConstraint(
            model_name='revenuemetricsnapshot',
            constraint=models.CheckConstraint(
                condition=models.Q(('adjustments__gte', 0)),
                name='rc_metric_adjustments_non_negative',
            ),
        ),
        migrations.AddConstraint(
            model_name='revenuemetricsnapshot',
            constraint=models.CheckConstraint(
                condition=models.Q(('denials__gte', 0)),
                name='rc_metric_denials_non_negative',
            ),
        ),
        migrations.AddConstraint(
            model_name='revenuemetricsnapshot',
            constraint=models.CheckConstraint(
                condition=models.Q(('write_offs__gte', 0)),
                name='rc_metric_writeoffs_non_negative',
            ),
        ),
        migrations.AddConstraint(
            model_name='revenuemetricsnapshot',
            constraint=models.CheckConstraint(
                condition=models.Q(('outstanding_ar__gte', 0)),
                name='rc_metric_ar_non_negative',
            ),
        ),
        migrations.AddIndex(
            model_name='scrubrule',
            index=models.Index(
                fields=['organization', 'is_active', 'priority'],
                name='rc_scrub_rule_org_active_idx',
            ),
        ),
        migrations.AddConstraint(
            model_name='scrubrule',
            constraint=models.UniqueConstraint(
                fields=('organization', 'code'), name='rc_scrub_rule_org_code_uniq'
            ),
        ),
        migrations.AddIndex(
            model_name='claimscrubfinding',
            index=models.Index(
                fields=['scrub', 'is_blocking', 'is_resolved'],
                name='rc_scrub_find_block_idx',
            ),
        ),
    ]
