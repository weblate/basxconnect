# Generated by Django 3.2.12 on 2022-04-04 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0027_auto_20211223_1948"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="term",
            options={"verbose_name": "Term", "verbose_name_plural": "Terms"},
        ),
        migrations.AlterOrderWithRespectTo(
            name="term",
            order_with_respect_to="vocabulary",
        ),
    ]
