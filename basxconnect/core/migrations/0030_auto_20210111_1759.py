# Generated by Django 3.1.5 on 2021-01-11 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_create_personnumbers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='personnumber',
            field=models.CharField(blank=True, max_length=255, unique=True, verbose_name='Person number'),
        ),
    ]