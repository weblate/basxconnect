# Generated by Django 3.2.10 on 2021-12-11 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer_integration', '0018_alter_synchronizationperson_sync_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='synchronizationresult',
            name='sync_completed_datetime',
            field=models.DateTimeField(null=True, verbose_name='Date and time'),
        ),
        migrations.AlterField(
            model_name='synchronizationresult',
            name='total_synchronized_persons',
            field=models.IntegerField(null=True, verbose_name='Number of persons in the mailer segment'),
        ),
    ]
