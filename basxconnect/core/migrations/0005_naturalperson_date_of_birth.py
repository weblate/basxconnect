# Generated by Django 3.1.1 on 2020-10-20 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_auto_20201019_1514"),
    ]

    operations = [
        migrations.AddField(
            model_name="naturalperson",
            name="date_of_birth",
            field=models.DateField(null=True, verbose_name="Date of Birth"),
        ),
    ]