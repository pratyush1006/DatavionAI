from django.db import migrations, models


class Migration(migrations.Migration):
    """Keep legacy organization billing relations distinct from SaaS billing."""

    dependencies = [
        (
            "organizations",
            "0003_organizationauditpolicy_organizationbillingaccount_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationbillingaccount",
            name="organization",
            field=models.OneToOneField(
                help_text="Organization billing profile.",
                on_delete=models.deletion.CASCADE,
                related_name="legacy_billing_account",
                to="organizations.organization",
            ),
        ),
        migrations.AlterField(
            model_name="organizationinvoice",
            name="organization",
            field=models.ForeignKey(
                help_text="Organization SaaS invoice.",
                on_delete=models.deletion.CASCADE,
                related_name="legacy_saas_invoices",
                to="organizations.organization",
            ),
        ),
    ]
