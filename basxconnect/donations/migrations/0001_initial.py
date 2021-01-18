# Generated by Django 3.1.5 on 2021-01-18 10:38

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0038_auto_20210116_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationImport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('currency', djmoney.models.fields.CurrencyField(default='XYZ', max_length=3)),
                ('date', models.DateField()),
                ('_import', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='donations.donationimport')),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.person')),
            ],
        ),
    ]
