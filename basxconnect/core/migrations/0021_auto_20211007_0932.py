# Generated by Django 3.2.4 on 2021-10-07 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_auto_20211005_1630"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="postal",
            name="valid_to",
        ),
        migrations.AddField(
            model_name="postal",
            name="valid_until",
            field=models.DateField(blank=True, null=True, verbose_name="Valid until"),
        ),
    ]
