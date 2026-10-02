import django.db.models.deletion
import uuid
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthcareInvoice',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('invoice_number', models.CharField(max_length=64)),
                (
                    'patient_reference',
                    models.CharField(blank=True, default='', max_length=128),
                ),
                (
                    'payer_name',
                    models.CharField(blank=True, default='', max_length=255),
                ),
                (
                    'claim_reference',
                    models.CharField(blank=True, default='', max_length=128),
                ),
                ('currency', models.CharField(default='INR', max_length=3)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('draft', 'Draft'),
                            ('finalized', 'Finalized'),
                            ('partially_paid', 'Partially Paid'),
                            ('paid', 'Paid'),
                            ('void', 'Void'),
                            ('written_off', 'Written Off'),
                        ],
                        default='draft',
                        max_length=32,
                    ),
                ),
                (
                    'subtotal',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'tax_total',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'discount_total',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'total',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'paid_total',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'adjustment_total',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'balance_due',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                ('due_date', models.DateField(blank=True, null=True)),
                ('finalized_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='rcm_healthcare_invoices',
                        to='organizations.organization',
                    ),
                ),
            ],
            options={
                'db_table': 'rcm_healthcare_invoices',
            },
        ),
        migrations.CreateModel(
            name='HealthcareAdjustment',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18)),
                (
                    'reason',
                    models.CharField(
                        choices=[
                            ('contractual', 'Contractual'),
                            ('discount', 'Discount'),
                            ('bad_debt', 'Bad Debt'),
                            ('refund', 'Refund'),
                            ('other', 'Other'),
                        ],
                        max_length=32,
                    ),
                ),
                ('reference', models.CharField(blank=True, default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='rcm_healthcare_adjustments',
                        to='organizations.organization',
                    ),
                ),
                (
                    'invoice',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='adjustments',
                        to='revenue_cycle_billing.healthcareinvoice',
                    ),
                ),
            ],
            options={
                'db_table': 'rcm_healthcare_adjustments',
            },
        ),
        migrations.CreateModel(
            name='HealthcareInvoiceLine',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('service_code', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=500)),
                (
                    'quantity',
                    models.DecimalField(
                        decimal_places=4, default=Decimal('1.0000'), max_digits=18
                    ),
                ),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=18)),
                (
                    'discount_amount',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'tax_amount',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'line_total',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'invoice',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='lines',
                        to='revenue_cycle_billing.healthcareinvoice',
                    ),
                ),
            ],
            options={
                'db_table': 'rcm_healthcare_invoice_lines',
            },
        ),
        migrations.CreateModel(
            name='HealthcarePayment',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18)),
                (
                    'method',
                    models.CharField(
                        choices=[
                            ('cash', 'Cash'),
                            ('card', 'Card'),
                            ('bank', 'Bank Transfer'),
                            ('upi', 'UPI'),
                            ('insurance', 'Insurance'),
                            ('other', 'Other'),
                        ],
                        max_length=32,
                    ),
                ),
                ('reference', models.CharField(blank=True, default='', max_length=128)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('pending', 'Pending'),
                            ('posted', 'Posted'),
                            ('void', 'Void'),
                            ('refunded', 'Refunded'),
                        ],
                        default='posted',
                        max_length=32,
                    ),
                ),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'invoice',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='payments',
                        to='revenue_cycle_billing.healthcareinvoice',
                    ),
                ),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='rcm_healthcare_payments',
                        to='organizations.organization',
                    ),
                ),
            ],
            options={
                'db_table': 'rcm_healthcare_payments',
            },
        ),
        migrations.CreateModel(
            name='HealthcarePaymentAllocation',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'invoice',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='payment_allocations',
                        to='revenue_cycle_billing.healthcareinvoice',
                    ),
                ),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='rcm_healthcare_payment_allocations',
                        to='organizations.organization',
                    ),
                ),
                (
                    'payment',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='allocations',
                        to='revenue_cycle_billing.healthcarepayment',
                    ),
                ),
            ],
            options={
                'db_table': 'rcm_healthcare_payment_allocations',
            },
        ),
        migrations.CreateModel(
            name='HealthcareRefund',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18)),
                ('reason', models.CharField(max_length=500)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('requested', 'Requested'),
                            ('approved', 'Approved'),
                            ('processed', 'Processed'),
                            ('rejected', 'Rejected'),
                        ],
                        default='requested',
                        max_length=32,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='rcm_healthcare_refunds',
                        to='organizations.organization',
                    ),
                ),
                (
                    'payment',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='refunds',
                        to='revenue_cycle_billing.healthcarepayment',
                    ),
                ),
            ],
            options={
                'db_table': 'rcm_healthcare_refunds',
            },
        ),
        migrations.CreateModel(
            name='HealthcareStatement',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('patient_reference', models.CharField(max_length=128)),
                ('period_start', models.DateField()),
                ('period_end', models.DateField()),
                (
                    'opening_balance',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'charges',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'payments',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'adjustments',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                (
                    'closing_balance',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=18
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='rcm_healthcare_statements',
                        to='organizations.organization',
                    ),
                ),
            ],
            options={
                'db_table': 'rcm_healthcare_statements',
            },
        ),
        migrations.CreateModel(
            name='HealthcareBillingAuditLog',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('event_type', models.CharField(max_length=128)),
                ('object_type', models.CharField(max_length=128)),
                ('object_id', models.CharField(max_length=128)),
                ('payload', models.JSONField(default=dict)),
                ('actor_id', models.CharField(blank=True, default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='rcm_healthcare_billing_audits',
                        to='organizations.organization',
                    ),
                ),
            ],
            options={
                'db_table': 'rcm_healthcare_billing_audit_logs',
                'indexes': [
                    models.Index(
                        fields=['organization', 'event_type'],
                        name='rcm_healthc_organiz_c8d511_idx',
                    ),
                    models.Index(
                        fields=['organization', 'object_type', 'object_id'],
                        name='rcm_healthc_organiz_3c5e68_idx',
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name='HealthcareBillingIdempotencyKey',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('workflow', models.CharField(max_length=160)),
                ('key', models.CharField(max_length=160)),
                (
                    'response_object_type',
                    models.CharField(blank=True, default='', max_length=128),
                ),
                (
                    'response_object_id',
                    models.CharField(blank=True, default='', max_length=128),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='rcm_healthcare_billing_idempotency',
                        to='organizations.organization',
                    ),
                ),
            ],
            options={
                'db_table': 'rcm_healthcare_billing_idempotency',
                'constraints': [
                    models.UniqueConstraint(
                        fields=('organization', 'workflow', 'key'),
                        name='rcm_hc_bill_idem_uniq',
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name='HealthcareBillingOutboxEvent',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'event_id',
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ('event_type', models.CharField(max_length=128)),
                ('aggregate_type', models.CharField(max_length=128)),
                ('aggregate_id', models.CharField(max_length=128)),
                ('payload', models.JSONField(default=dict)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('pending', 'Pending'),
                            ('processing', 'Processing'),
                            ('published', 'Published'),
                            ('failed', 'Failed'),
                        ],
                        default='pending',
                        max_length=20,
                    ),
                ),
                ('attempts', models.PositiveIntegerField(default=0)),
                ('available_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('last_error', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='rcm_healthcare_billing_outbox',
                        to='organizations.organization',
                    ),
                ),
            ],
            options={
                'db_table': 'rcm_healthcare_billing_outbox',
                'indexes': [
                    models.Index(
                        fields=['organization', 'status', 'available_at'],
                        name='rcm_healthc_organiz_96661f_idx',
                    )
                ],
            },
        ),
        migrations.AddIndex(
            model_name='healthcareinvoice',
            index=models.Index(
                fields=['organization', 'status'], name='rcm_healthc_organiz_531a5d_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='healthcareinvoice',
            index=models.Index(
                fields=['organization', 'patient_reference'],
                name='rcm_healthc_organiz_7adca0_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='healthcareinvoice',
            index=models.Index(
                fields=['organization', 'claim_reference'],
                name='rcm_healthc_organiz_eba9a8_idx',
            ),
        ),
        migrations.AddConstraint(
            model_name='healthcareinvoice',
            constraint=models.UniqueConstraint(
                fields=('organization', 'invoice_number'),
                name='rcm_hc_invoice_org_number_uniq',
            ),
        ),
        migrations.AddConstraint(
            model_name='healthcarepayment',
            constraint=models.UniqueConstraint(
                fields=('organization', 'reference'),
                name='rcm_hc_payment_org_reference_uniq',
            ),
        ),
        migrations.AddIndex(
            model_name='healthcarestatement',
            index=models.Index(
                fields=['organization', 'patient_reference'],
                name='rcm_healthc_organiz_e91999_idx',
            ),
        ),
    ]
