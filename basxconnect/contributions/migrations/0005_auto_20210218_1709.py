# Generated by Django 3.1.5 on 2021-02-18 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contributions', '0004_auto_20210218_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='creditaccount',
            field=models.CharField(max_length=32, verbose_name='Credit Account'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='debitaccount',
            field=models.CharField(max_length=32, verbose_name='Debit Account'),
        ),
    ]
