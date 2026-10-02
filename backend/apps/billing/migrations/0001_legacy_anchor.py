from django.db import migrations


class Migration(migrations.Migration):
    """No-op replacement for the retired healthcare billing initial migration."""

    replaces = [("billing", "0001_initial")]
    initial = True
    operations = []
