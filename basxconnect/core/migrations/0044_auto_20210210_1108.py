# Generated by Django 3.1.5 on 2021-02-10 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0043_auto_20210208_1540"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postal",
            name="city",
            field=models.CharField(blank=True, max_length=255, verbose_name="City"),
        ),
    ]
