from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "organizations",
            "0004_namespace_legacy_billing_relations",
        ),
        (
            "tenancy",
            "0003_usertenantpreference",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="tenant",
            field=models.ForeignKey(
                db_index=True,
                help_text="SaaS tenant owning this organization.",
                on_delete=models.CASCADE,
                related_name="organizations",
                to="tenancy.tenant",
            ),
        ),
    ]
