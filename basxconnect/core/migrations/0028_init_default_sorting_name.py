# Generated by Django 3.2.8 on 2021-12-10 18:42

from django.db import migrations


class Migration(migrations.Migration):
    def init_default_sorting_name(apps, _):
        naturalpersons = apps.get_model("core.NaturalPerson").objects.all()
        other_persons = (
            *apps.get_model("core.LegalPerson").objects.all(),
            *apps.get_model("core.PersonAssociation").objects.all(),
        )

        for person in naturalpersons:
            person.default_sorting_name = person.last_name
            person.save()

        for person in other_persons:
            person.default_sorting_name = person.name
            person.save()

    dependencies = [
        ("core", "0027_auto_20211211_0140"),
    ]

    operations = [migrations.RunPython(init_default_sorting_name)]
