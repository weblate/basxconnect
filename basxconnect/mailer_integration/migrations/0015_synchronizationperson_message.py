# Generated by Django 3.2.4 on 2021-11-22 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailer_integration", "0014_rename_mailingpreferences_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="synchronizationperson",
            name="message",
            field=models.CharField(blank=True, max_length=255, verbose_name="Message"),
        ),
    ]
