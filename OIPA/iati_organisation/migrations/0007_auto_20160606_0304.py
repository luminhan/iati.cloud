# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 03:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iati_codelists', '0005_auto_20160602_1644'),
        ('iati_vocabulary', '0005_result-indicator-reference'),
        ('geodata', '0001_initial'),
        ('iati_organisation', '0006_auto_20160602_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipientRegionBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vocabulary_uri', models.URLField(blank=True, null=True)),
                ('period_start', models.DateField(null=True)),
                ('period_end', models.DateField(null=True)),
                ('value', models.DecimalField(decimal_places=2, default=None, max_digits=14, null=True)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.Currency')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_region_budget', to='iati_organisation.Organisation')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geodata.Region')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.BudgetStatus')),
                ('vocabulary', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='iati_vocabulary.RegionVocabulary')),
            ],
        ),
        migrations.CreateModel(
            name='TotalExpenditure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_start', models.DateField(null=True)),
                ('period_end', models.DateField(null=True)),
                ('value_date', models.DateField(null=True)),
                ('value', models.DecimalField(decimal_places=2, default=None, max_digits=14, null=True)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.Currency')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total_expenditure', to='iati_organisation.Organisation')),
            ],
        ),
        migrations.AddField(
            model_name='documentlink',
            name='iso_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipientcountrybudget',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.BudgetStatus'),
        ),
        migrations.AddField(
            model_name='recipientorgbudget',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.BudgetStatus'),
        ),
        migrations.AddField(
            model_name='totalbudget',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='iati_codelists.BudgetStatus'),
        ),
    ]