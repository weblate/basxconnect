# Generated by Django 3.1.5 on 2021-02-18 09:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contributions", "0003_auto_20210216_1538"),
    ]

    operations = [
        migrations.AddField(
            model_name="contributionimport",
            name="importfile",
            field=models.FileField(default="", upload_to=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="contributionimport",
            name="date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]