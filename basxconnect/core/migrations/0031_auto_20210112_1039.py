# Generated by Django 3.1.5 on 2021-01-12 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0030_auto_20210111_1759"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postal",
            name="address",
            field=models.TextField(max_length=255, verbose_name="Address"),
        ),
    ]
