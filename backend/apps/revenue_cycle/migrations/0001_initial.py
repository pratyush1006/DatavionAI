import apps.core.models.managers
import django.core.validators
import django.db.models.deletion
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('patient_core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentPosting',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('payer_name', models.CharField(blank=True, max_length=200)),
                ('payer_claim_reference', models.CharField(blank=True, max_length=100)),
                (
                    'source',
                    models.CharField(
                        choices=[
                            ('manual', 'Manual'),
                            ('era', 'ERA'),
                            ('eob', 'EOB'),
                            ('patient', 'Patient'),
                            ('adjustment', 'Adjustment'),
                        ],
                        default='manual',
                        max_length=20,
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('pending', 'Pending'),
                            ('posted', 'Posted'),
                            ('reversed', 'Reversed'),
                            ('voided', 'Voided'),
                        ],
                        db_index=True,
                        default='pending',
                        max_length=20,
                    ),
                ),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                (
                    'adjustment_amount',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=14
                    ),
                ),
                ('posted_at', models.DateTimeField(blank=True, null=True)),
                ('reversed_at', models.DateTimeField(blank=True, null=True)),
                ('external_reference', models.CharField(blank=True, max_length=150)),
                ('idempotency_key', models.CharField(max_length=150)),
                ('notes', models.TextField(blank=True)),
                ('reversal_reason', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'revenue_cycle_payment_postings',
                'ordering': ('-created_at',),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='PriorAuthorization',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                (
                    'eligibility_reference',
                    models.UUIDField(blank=True, db_index=True, null=True),
                ),
                ('payer_id', models.CharField(db_index=True, max_length=100)),
                ('payer_name', models.CharField(blank=True, max_length=255)),
                ('member_id', models.CharField(db_index=True, max_length=100)),
                ('policy_number', models.CharField(blank=True, max_length=100)),
                ('group_number', models.CharField(blank=True, max_length=100)),
                ('procedure_code', models.CharField(db_index=True, max_length=50)),
                ('service_description', models.CharField(blank=True, max_length=500)),
                ('place_of_service', models.CharField(blank=True, max_length=20)),
                ('rendering_provider_npi', models.CharField(blank=True, max_length=20)),
                ('clinical_indication', models.TextField(blank=True)),
                (
                    'authorization_method',
                    models.CharField(
                        choices=[
                            ('manual', 'manual'),
                            ('payer_api', 'payer_api'),
                            ('clearinghouse', 'clearinghouse'),
                            ('portal', 'portal'),
                            ('import', 'import'),
                        ],
                        default='manual',
                        max_length=30,
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('pending', 'pending'),
                            ('in_review', 'in_review'),
                            ('submitted', 'submitted'),
                            ('approved', 'approved'),
                            ('denied', 'denied'),
                            ('expired', 'expired'),
                            ('cancelled', 'cancelled'),
                            ('inactive', 'inactive'),
                        ],
                        db_index=True,
                        default='pending',
                        max_length=30,
                    ),
                ),
                (
                    'outcome',
                    models.CharField(
                        choices=[
                            ('approved', 'approved'),
                            ('denied', 'denied'),
                            ('pended', 'pended'),
                            ('not_required', 'not_required'),
                            ('unknown', 'unknown'),
                        ],
                        db_index=True,
                        default='unknown',
                        max_length=30,
                    ),
                ),
                ('requested_service_date', models.DateField(blank=True, null=True)),
                ('requested_units', models.PositiveIntegerField(blank=True, null=True)),
                ('approved_units', models.PositiveIntegerField(blank=True, null=True)),
                (
                    'requested_amount',
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=14, null=True
                    ),
                ),
                (
                    'authorization_number',
                    models.CharField(blank=True, db_index=True, max_length=100),
                ),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('decision_reason', models.TextField(blank=True)),
                (
                    'requested_at',
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ('submitted_at', models.DateTimeField(blank=True, null=True)),
                ('decided_at', models.DateTimeField(blank=True, null=True)),
                ('response_code', models.CharField(blank=True, max_length=100)),
                ('response_message', models.TextField(blank=True)),
                ('response_payload', models.JSONField(blank=True, default=dict)),
                ('request_reference', models.CharField(db_index=True, max_length=100)),
                ('idempotency_key', models.CharField(db_index=True, max_length=255)),
                ('failure_reason', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'revenue_cycle_prior_authorization',
                'ordering': ('-requested_at',),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='RevenueCycleIntegrationRecord',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                (
                    'event_type',
                    models.CharField(
                        choices=[
                            ('PATIENT_CONTEXT', 'Patient Context'),
                            ('CLAIM_CONTEXT', 'Claim Context'),
                            ('PAYMENT_CONTEXT', 'Payment Context'),
                            ('AR_CONTEXT', 'AR Context'),
                            ('ANALYTICS_CONTEXT', 'Analytics Context'),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    'source',
                    models.CharField(
                        choices=[
                            ('ELIGIBILITY', 'Eligibility'),
                            ('INSURANCE_VERIFICATION', 'Insurance Verification'),
                            ('PRIOR_AUTHORIZATION', 'Prior Authorization'),
                            ('CHARGE_CAPTURE', 'Charge Capture'),
                            ('CODING', 'Coding'),
                            ('CLAIM_SCRUBBING', 'Claim Scrubbing'),
                            ('CLAIM_SUBMISSION', 'Claim Submission'),
                            ('PAYMENT_POSTING', 'Payment Posting'),
                            ('ERA', 'ERA'),
                            ('DENIALS', 'Denials'),
                            ('APPEALS', 'Appeals'),
                            ('ACCOUNTS_RECEIVABLE', 'Accounts Receivable'),
                            ('REVENUE_ANALYTICS', 'Revenue Analytics'),
                        ],
                        max_length=30,
                    ),
                ),
                ('event_name', models.CharField(max_length=150)),
                ('aggregate_id', models.UUIDField()),
                ('idempotency_key', models.CharField(max_length=200)),
                ('payload', models.JSONField(default=dict)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('PENDING', 'Pending'),
                            ('PROCESSED', 'Processed'),
                            ('FAILED', 'Failed'),
                            ('IGNORED', 'Ignored'),
                        ],
                        db_index=True,
                        default='PENDING',
                        max_length=20,
                    ),
                ),
                ('attempts', models.PositiveIntegerField(default=0)),
                ('last_error', models.TextField(blank=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'revenue_cycle_integration_records',
                'ordering': ('-created_at',),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='RevenueMetricSnapshot',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                (
                    'period',
                    models.CharField(
                        choices=[
                            ('DAY', 'Day'),
                            ('WEEK', 'Week'),
                            ('MONTH', 'Month'),
                            ('QUARTER', 'Quarter'),
                            ('YEAR', 'Year'),
                        ],
                        max_length=10,
                    ),
                ),
                ('period_start', models.DateField()),
                ('period_end', models.DateField()),
                (
                    'gross_charges',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=16
                    ),
                ),
                (
                    'payments',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=16
                    ),
                ),
                (
                    'adjustments',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=16
                    ),
                ),
                (
                    'denials',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=16
                    ),
                ),
                (
                    'write_offs',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=16
                    ),
                ),
                (
                    'outstanding_ar',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=16
                    ),
                ),
                ('encounter_count', models.PositiveBigIntegerField(default=0)),
                ('claim_count', models.PositiveBigIntegerField(default=0)),
                ('denied_claim_count', models.PositiveBigIntegerField(default=0)),
                ('paid_claim_count', models.PositiveBigIntegerField(default=0)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'revenue_cycle_metric_snapshots',
                'ordering': ('-period_end', '-generated_at'),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='ScrubRule',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('code', models.CharField(max_length=80)),
                ('name', models.CharField(max_length=160)),
                (
                    'rule_type',
                    models.CharField(
                        choices=[
                            ('required', 'Required'),
                            ('range', 'Range'),
                            ('format', 'Format'),
                            ('consistency', 'Consistency'),
                            ('codeset', 'Code Set'),
                        ],
                        max_length=30,
                    ),
                ),
                ('field_name', models.CharField(max_length=120)),
                ('configuration', models.JSONField(blank=True, default=dict)),
                ('severity', models.CharField(default='error', max_length=20)),
                ('is_blocking', models.BooleanField(default=True)),
                ('priority', models.PositiveIntegerField(default=100)),
            ],
            options={
                'db_table': 'revenue_cycle_scrub_rules',
                'ordering': ('priority', 'code'),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='Appeal',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('claim_reference', models.CharField(max_length=120)),
                ('payer_name', models.CharField(max_length=200)),
                ('appeal_number', models.CharField(max_length=100)),
                ('denial_reference', models.CharField(blank=True, max_length=120)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('draft', 'Draft'),
                            ('submitted', 'Submitted'),
                            ('under_review', 'Under Review'),
                            ('pending_information', 'Pending Information'),
                            ('approved', 'Approved'),
                            ('partially_approved', 'Partially Approved'),
                            ('denied', 'Denied'),
                            ('withdrawn', 'Withdrawn'),
                            ('closed', 'Closed'),
                        ],
                        db_index=True,
                        default='draft',
                        max_length=32,
                    ),
                ),
                (
                    'priority',
                    models.CharField(db_index=True, default='normal', max_length=16),
                ),
                ('reason', models.TextField()),
                ('clinical_summary', models.TextField(blank=True)),
                (
                    'requested_amount',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=14
                    ),
                ),
                (
                    'approved_amount',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=14
                    ),
                ),
                ('submitted_at', models.DateTimeField(blank=True, null=True)),
                ('decided_at', models.DateTimeField(blank=True, null=True)),
                ('decision_reason', models.TextField(blank=True)),
                ('idempotency_key', models.CharField(max_length=120)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                (
                    'created_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='created_revenue_cycle_appeals',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_appeals',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_appeals',
                        to='patient_core.patient',
                    ),
                ),
                (
                    'updated_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='updated_revenue_cycle_appeals',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_appeals',
                'ordering': ('-created_at',),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='ARAccount',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('account_number', models.CharField(max_length=40)),
                ('currency', models.CharField(default='INR', max_length=3)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('OPEN', 'Open'),
                            ('ON_HOLD', 'On Hold'),
                            ('PAID', 'Paid'),
                            ('WRITTEN_OFF', 'Written Off'),
                            ('CLOSED', 'Closed'),
                        ],
                        db_index=True,
                        default='OPEN',
                        max_length=20,
                    ),
                ),
                (
                    'balance_amount',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=14
                    ),
                ),
                (
                    'total_charges',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=14
                    ),
                ),
                (
                    'total_payments',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=14
                    ),
                ),
                (
                    'total_adjustments',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=14
                    ),
                ),
                (
                    'total_write_offs',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=14
                    ),
                ),
                (
                    'hold_reason',
                    models.CharField(
                        blank=True,
                        choices=[
                            ('MANUAL_REVIEW', 'Manual Review'),
                            ('DISPUTE', 'Dispute'),
                            ('INSURANCE', 'Insurance'),
                            ('COLLECTIONS', 'Collections'),
                        ],
                        max_length=30,
                    ),
                ),
                ('hold_note', models.TextField(blank=True)),
                ('opened_at', models.DateTimeField(auto_now_add=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('version', models.PositiveBigIntegerField(default=1)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_ar_accounts',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_ar_accounts',
                        to='patient_core.patient',
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_ar_accounts',
                'ordering': ('-created_at',),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='ARActivityLog',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('action', models.CharField(max_length=30)),
                ('details', models.JSONField(blank=True, default=dict)),
                ('performed_at', models.DateTimeField(auto_now_add=True)),
                (
                    'account',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='activity_logs',
                        to='revenue_cycle.araccount',
                    ),
                ),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_ar_activity_logs',
                        to='organizations.organization',
                    ),
                ),
                (
                    'performed_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='revenue_cycle_ar_activity_logs',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_ar_activity_logs',
                'ordering': ('-performed_at',),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='ARTransaction',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('transaction_number', models.CharField(max_length=50)),
                (
                    'transaction_type',
                    models.CharField(
                        choices=[
                            ('CHARGE', 'Charge'),
                            ('PAYMENT', 'Payment'),
                            ('ADJUSTMENT', 'Adjustment'),
                            ('DENIAL', 'Denial'),
                            ('WRITE_OFF', 'Write Off'),
                            ('REFUND', 'Refund'),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[('POSTED', 'Posted'), ('REVERSED', 'Reversed')],
                        default='POSTED',
                        max_length=20,
                    ),
                ),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('transaction_date', models.DateTimeField()),
                ('source_type', models.CharField(blank=True, max_length=50)),
                ('source_id', models.UUIDField(blank=True, null=True)),
                ('external_reference', models.CharField(blank=True, max_length=100)),
                ('note', models.TextField(blank=True)),
                ('reversed_at', models.DateTimeField(blank=True, null=True)),
                (
                    'account',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='transactions',
                        to='revenue_cycle.araccount',
                    ),
                ),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_ar_transactions',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_ar_transactions',
                        to='patient_core.patient',
                    ),
                ),
                (
                    'reversed_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='reversed_rc_ar_transactions',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_ar_transactions',
                'ordering': ('-transaction_date', '-created_at'),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('tenant_id', models.UUIDField(db_index=True)),
                ('service_code', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=500)),
                (
                    'quantity',
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=12,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal('0.001'))
                        ],
                    ),
                ),
                (
                    'unit_price',
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=14,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal('0.00'))
                        ],
                    ),
                ),
                (
                    'total_amount',
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=16,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal('0.00'))
                        ],
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('draft', 'draft'),
                            ('ready', 'ready'),
                            ('submitted', 'submitted'),
                            ('voided', 'voided'),
                        ],
                        db_index=True,
                        default='draft',
                        max_length=32,
                    ),
                ),
                (
                    'idempotency_key',
                    models.CharField(
                        blank=True, db_index=True, max_length=128, null=True
                    ),
                ),
                ('captured_at', models.DateTimeField(blank=True, null=True)),
                ('voided_at', models.DateTimeField(blank=True, null=True)),
                ('void_reason', models.CharField(blank=True, max_length=500)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_charges',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_charges',
                        to='patient_core.patient',
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_charge_capture_charges',
                'ordering': ('-created_at',),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='ClaimScrub',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('claim_reference', models.CharField(max_length=120)),
                ('idempotency_key', models.CharField(max_length=160)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('pending', 'Pending'),
                            ('running', 'Running'),
                            ('passed', 'Passed'),
                            ('failed', 'Failed'),
                            ('overridden', 'Overridden'),
                        ],
                        db_index=True,
                        default='pending',
                        max_length=20,
                    ),
                ),
                ('input_snapshot', models.JSONField(blank=True, default=dict)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('override_reason', models.TextField(blank=True)),
                (
                    'created_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='created_claim_scrubs',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='revenue_cycle_claim_scrubs',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_claim_scrubs',
                        to='patient_core.patient',
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_claim_scrubs',
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='ClaimScrubFinding',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('field_name', models.CharField(max_length=120)),
                ('message', models.TextField()),
                (
                    'severity',
                    models.CharField(
                        choices=[
                            ('info', 'Info'),
                            ('warning', 'Warning'),
                            ('error', 'Error'),
                            ('critical', 'Critical'),
                        ],
                        max_length=20,
                    ),
                ),
                ('is_blocking', models.BooleanField(default=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('observed_value', models.JSONField(blank=True, null=True)),
                (
                    'scrub',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='findings',
                        to='revenue_cycle.claimscrub',
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_claim_scrub_findings',
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='ClaimSubmission',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('claim_reference', models.CharField(max_length=100)),
                ('payer_id', models.CharField(max_length=100)),
                ('payer_name', models.CharField(blank=True, max_length=200)),
                (
                    'submission_method',
                    models.CharField(
                        choices=[
                            ('edi', 'EDI'),
                            ('api', 'API'),
                            ('portal', 'Portal'),
                            ('manual', 'Manual'),
                        ],
                        default='edi',
                        max_length=20,
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('pending', 'Pending'),
                            ('validated', 'Validated'),
                            ('submitting', 'Submitting'),
                            ('submitted', 'Submitted'),
                            ('accepted', 'Accepted'),
                            ('rejected', 'Rejected'),
                            ('failed', 'Failed'),
                            ('cancelled', 'Cancelled'),
                        ],
                        db_index=True,
                        default='pending',
                        max_length=20,
                    ),
                ),
                ('payload', models.JSONField(blank=True, default=dict)),
                ('response_data', models.JSONField(blank=True, default=dict)),
                (
                    'external_submission_id',
                    models.CharField(blank=True, max_length=150),
                ),
                ('rejection_code', models.CharField(blank=True, max_length=100)),
                ('rejection_reason', models.TextField(blank=True)),
                ('submitted_at', models.DateTimeField(blank=True, null=True)),
                ('accepted_at', models.DateTimeField(blank=True, null=True)),
                ('failed_at', models.DateTimeField(blank=True, null=True)),
                ('cancelled_at', models.DateTimeField(blank=True, null=True)),
                ('idempotency_key', models.CharField(max_length=150)),
                (
                    'created_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='created_revenue_cycle_claim_submissions',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='revenue_cycle_claim_submissions',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_claim_submissions',
                        to='patient_core.patient',
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_claim_submissions',
                'ordering': ('-created_at',),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='CodingRecord',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                (
                    'coding_type',
                    models.CharField(
                        choices=[
                            ('professional', 'Professional'),
                            ('facility', 'Facility'),
                            ('outpatient', 'Outpatient'),
                            ('inpatient', 'Inpatient'),
                            ('other', 'Other'),
                        ],
                        default='professional',
                        max_length=32,
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('draft', 'Draft'),
                            ('assigned', 'Assigned'),
                            ('in_review', 'In Review'),
                            ('coded', 'Coded'),
                            ('validated', 'Validated'),
                            ('rejected', 'Rejected'),
                            ('released', 'Released'),
                            ('voided', 'Voided'),
                        ],
                        db_index=True,
                        default='draft',
                        max_length=32,
                    ),
                ),
                ('source_reference', models.CharField(db_index=True, max_length=128)),
                ('service_date', models.DateField(db_index=True)),
                ('encounter_type', models.CharField(blank=True, max_length=64)),
                ('clinical_summary', models.TextField(blank=True)),
                ('documentation', models.JSONField(blank=True, default=dict)),
                ('coding_notes', models.TextField(blank=True)),
                ('rejection_reason', models.TextField(blank=True)),
                ('idempotency_key', models.CharField(max_length=128)),
                ('assigned_at', models.DateTimeField(blank=True, null=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('validated_at', models.DateTimeField(blank=True, null=True)),
                ('released_at', models.DateTimeField(blank=True, null=True)),
                ('voided_at', models.DateTimeField(blank=True, null=True)),
                (
                    'assigned_to',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='assigned_revenue_cycle_records',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_records',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_records',
                        to='patient_core.patient',
                    ),
                ),
                (
                    'released_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='released_revenue_cycle_records',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'reviewed_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='reviewed_revenue_cycle_records',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'validated_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='validated_revenue_cycle_records',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_records',
                'ordering': ('-service_date', '-created_at'),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='CodeAssignment',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                (
                    'code_system',
                    models.CharField(
                        choices=[
                            ('icd10cm', 'ICD-10-CM'),
                            ('icd10pcs', 'ICD-10-PCS'),
                            ('cpt', 'CPT'),
                            ('hcpcs', 'HCPCS'),
                            ('modifier', 'Modifier'),
                            ('other', 'Other'),
                        ],
                        max_length=32,
                    ),
                ),
                ('code', models.CharField(max_length=64)),
                ('description', models.CharField(blank=True, max_length=512)),
                ('sequence', models.PositiveIntegerField(default=1)),
                ('present_on_admission', models.BooleanField(blank=True, null=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('evidence', models.JSONField(blank=True, default=dict)),
                (
                    'coding_record',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='code_assignments',
                        to='revenue_cycle.codingrecord',
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_code_assignments',
                'ordering': ('sequence', 'created_at'),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='Denial',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                (
                    'claim_submission_id',
                    models.UUIDField(blank=True, db_index=True, null=True),
                ),
                ('external_claim_id', models.CharField(blank=True, max_length=100)),
                ('payer_name', models.CharField(max_length=255)),
                ('denial_code', models.CharField(db_index=True, max_length=50)),
                ('denial_reason', models.TextField()),
                (
                    'amount',
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=14,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal('0'))
                        ],
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('open', 'Open'),
                            ('under_review', 'Under Review'),
                            ('action_required', 'Action Required'),
                            ('appeal_pending', 'Appeal Pending'),
                            ('resolved', 'Resolved'),
                            ('written_off', 'Written Off'),
                        ],
                        db_index=True,
                        default='open',
                        max_length=30,
                    ),
                ),
                (
                    'priority',
                    models.CharField(
                        choices=[
                            ('low', 'Low'),
                            ('normal', 'Normal'),
                            ('high', 'High'),
                            ('urgent', 'Urgent'),
                        ],
                        db_index=True,
                        default='normal',
                        max_length=20,
                    ),
                ),
                ('received_at', models.DateTimeField()),
                ('due_at', models.DateTimeField(blank=True, null=True)),
                ('resolution_note', models.TextField(blank=True)),
                ('external_reference', models.CharField(blank=True, max_length=100)),
                ('idempotency_key', models.CharField(max_length=128)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                (
                    'created_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='created_revenue_cycle_denials',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_denials',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_denials',
                        to='patient_core.patient',
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_denials',
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='Eligibility',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('payer_id', models.CharField(db_index=True, max_length=100)),
                ('payer_name', models.CharField(blank=True, max_length=255)),
                ('member_id', models.CharField(db_index=True, max_length=100)),
                ('group_number', models.CharField(blank=True, max_length=100)),
                ('subscriber_name', models.CharField(blank=True, max_length=255)),
                (
                    'subscriber_relationship',
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    'requested_at',
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('coverage_start', models.DateField(blank=True, null=True)),
                ('coverage_end', models.DateField(blank=True, null=True)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('pending', 'pending'),
                            ('in_progress', 'in_progress'),
                            ('verified', 'verified'),
                            ('failed', 'failed'),
                            ('inactive', 'inactive'),
                        ],
                        db_index=True,
                        default='pending',
                        max_length=30,
                    ),
                ),
                (
                    'coverage_status',
                    models.CharField(
                        choices=[
                            ('active', 'active'),
                            ('inactive', 'inactive'),
                            ('unknown', 'unknown'),
                            ('not_found', 'not_found'),
                        ],
                        db_index=True,
                        default='unknown',
                        max_length=30,
                    ),
                ),
                (
                    'copay_amount',
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    'deductible_amount',
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ('response_code', models.CharField(blank=True, max_length=100)),
                ('response_message', models.TextField(blank=True)),
                ('response_payload', models.JSONField(blank=True, default=dict)),
                ('request_reference', models.CharField(db_index=True, max_length=100)),
                ('idempotency_key', models.CharField(db_index=True, max_length=255)),
                ('failure_reason', models.TextField(blank=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_eligibility',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_eligibility',
                        to='patient_core.patient',
                    ),
                ),
                (
                    'verified_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='revenue_cycle_eligibility_verified',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_eligibility',
                'ordering': ('-requested_at',),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='ERA',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                ('payer_name', models.CharField(max_length=200)),
                ('payer_identifier', models.CharField(blank=True, max_length=100)),
                ('trace_number', models.CharField(max_length=100)),
                ('check_or_eft_number', models.CharField(blank=True, max_length=100)),
                (
                    'source',
                    models.CharField(
                        choices=[
                            ('edi_835', 'EDI 835'),
                            ('portal', 'Payer Portal'),
                            ('manual', 'Manual'),
                            ('api', 'API'),
                        ],
                        default='edi_835',
                        max_length=20,
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('received', 'Received'),
                            ('validated', 'Validated'),
                            ('posting', 'Posting'),
                            ('posted', 'Posted'),
                            ('failed', 'Failed'),
                            ('reversed', 'Reversed'),
                        ],
                        db_index=True,
                        default='received',
                        max_length=20,
                    ),
                ),
                (
                    'payment_amount',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=14
                    ),
                ),
                (
                    'adjustment_amount',
                    models.DecimalField(
                        decimal_places=2, default=Decimal('0.00'), max_digits=14
                    ),
                ),
                ('received_at', models.DateTimeField()),
                ('validated_at', models.DateTimeField(blank=True, null=True)),
                ('posted_at', models.DateTimeField(blank=True, null=True)),
                ('reversed_at', models.DateTimeField(blank=True, null=True)),
                ('external_reference', models.CharField(blank=True, max_length=150)),
                ('idempotency_key', models.CharField(max_length=150)),
                ('raw_payload', models.JSONField(blank=True, default=dict)),
                ('validation_errors', models.JSONField(blank=True, default=list)),
                ('notes', models.TextField(blank=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_eras',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_eras',
                        to='patient_core.patient',
                    ),
                ),
                (
                    'processed_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='revenue_cycle_eras',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_eras',
                'ordering': ('-received_at', '-created_at'),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
        migrations.CreateModel(
            name='InsuranceVerification',
            fields=[
                (
                    'is_active',
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text='Indicates whether the entity is available for normal operations.',
                        verbose_name='Active',
                    ),
                ),
                (
                    'is_deleted',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        editable=False,
                        verbose_name='Deleted',
                    ),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(
                        blank=True, editable=False, null=True, verbose_name='Deleted At'
                    ),
                ),
                (
                    'deleted_by_id',
                    models.UUIDField(
                        blank=True, editable=False, null=True, verbose_name='Deleted By'
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        help_text='Timestamp when the record was created.',
                        verbose_name='Created At',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        help_text='Timestamp when the record was last updated.',
                        verbose_name='Updated At',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Globally unique UUID v4 identifier.',
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='Identifier',
                    ),
                ),
                (
                    'eligibility_reference',
                    models.UUIDField(blank=True, db_index=True, null=True),
                ),
                ('payer_id', models.CharField(db_index=True, max_length=100)),
                ('payer_name', models.CharField(blank=True, max_length=255)),
                ('member_id', models.CharField(db_index=True, max_length=100)),
                ('policy_number', models.CharField(blank=True, max_length=100)),
                ('group_number', models.CharField(blank=True, max_length=100)),
                ('subscriber_name', models.CharField(blank=True, max_length=255)),
                (
                    'subscriber_relationship',
                    models.CharField(blank=True, max_length=50),
                ),
                (
                    'verification_method',
                    models.CharField(
                        choices=[
                            ('manual', 'manual'),
                            ('payer_api', 'payer_api'),
                            ('clearinghouse', 'clearinghouse'),
                            ('import', 'import'),
                        ],
                        default='manual',
                        max_length=30,
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('pending', 'pending'),
                            ('in_progress', 'in_progress'),
                            ('verified', 'verified'),
                            ('failed', 'failed'),
                            ('expired', 'expired'),
                            ('inactive', 'inactive'),
                        ],
                        db_index=True,
                        default='pending',
                        max_length=30,
                    ),
                ),
                (
                    'outcome',
                    models.CharField(
                        choices=[
                            ('active', 'active'),
                            ('inactive', 'inactive'),
                            ('not_found', 'not_found'),
                            ('unknown', 'unknown'),
                        ],
                        db_index=True,
                        default='unknown',
                        max_length=30,
                    ),
                ),
                (
                    'requested_at',
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('coverage_start', models.DateField(blank=True, null=True)),
                ('coverage_end', models.DateField(blank=True, null=True)),
                (
                    'copay_amount',
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    'deductible_amount',
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    'coinsurance_percent',
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                ('prior_authorization_required', models.BooleanField(default=False)),
                ('response_code', models.CharField(blank=True, max_length=100)),
                ('response_message', models.TextField(blank=True)),
                ('response_payload', models.JSONField(blank=True, default=dict)),
                ('request_reference', models.CharField(db_index=True, max_length=100)),
                ('idempotency_key', models.CharField(db_index=True, max_length=255)),
                ('failure_reason', models.TextField(blank=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_insurance_verifications',
                        to='organizations.organization',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='revenue_cycle_insurance_verifications',
                        to='patient_core.patient',
                    ),
                ),
                (
                    'verified_by',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='revenue_cycle_insurance_verifications_verified',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'db_table': 'revenue_cycle_insurance_verification',
                'ordering': ('-requested_at',),
            },
            managers=[
                ('objects', apps.core.models.managers.SoftDeleteManager()),
                ('all_objects', apps.core.models.managers.AllObjectsManager()),
                ('deleted_objects', apps.core.models.managers.DeletedObjectsManager()),
            ],
        ),
    ]
