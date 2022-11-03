# Generated by Django 4.0.6 on 2022-11-03 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0032_alter_historicallegalperson_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalnaturalperson",
            name="maiden_name",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Maiden Name"
            ),
        ),
        migrations.AddField(
            model_name="naturalperson",
            name="maiden_name",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Maiden Name"
            ),
        ),
    ]
