# Generated by Django 4.1.7 on 2023-04-05 04:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("basxconnect_invoicing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="note",
            field=models.TextField(
                blank=True,
                help_text="Can be displayed on invoice and/or receipt",
                verbose_name="Note to client",
            ),
        ),
    ]