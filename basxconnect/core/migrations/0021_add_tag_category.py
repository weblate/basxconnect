# Generated by Django 3.1.4 on 2020-12-12 13:59

from django.db import migrations


class Migration(migrations.Migration):
    def create_category(apps, schema_editor):
        Category = apps.get_model("core.Category")
        Category.objects.create(
            name="Correspondence Language", slug="correspondence_language"
        )
        Category.objects.create(
            name="Communication channels", slug="communication_channels"
        )

    dependencies = [
        ("core", "0020_auto_20201207_2136"),
    ]

    operations = [migrations.RunPython(create_category, migrations.RunPython.noop)]