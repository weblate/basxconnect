# Generated by Django 3.2.4 on 2021-08-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailer_integration", "0006_alter_mailingpreferences_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailingpreferences",
            name="interests",
            field=models.ManyToManyField(blank=True, to="mailer_integration.Interest"),
        ),
    ]
