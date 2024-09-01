from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NginxLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip_address", models.GenericIPAddressField()),
                ("date", models.DateTimeField()),
                ("http_method", models.CharField(max_length=10)),
                ("uri", models.TextField()),
                ("response_code", models.IntegerField()),
                ("response_size", models.BigIntegerField()),
            ],
        ),
    ]
