# Generated by Django 3.1 on 2020-11-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_create_initial_organization"),
    ]

    operations = [
        migrations.AddField(
            model_name="juristicperson",
            name="name_addition",
            field=models.CharField(blank=True, max_length=255, verbose_name="Addition"),
        ),
    ]