# Generated by Django 2.0.13 on 2019-09-30 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iati_organisation', '0005_organisation_dataset'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='last_updated_model',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]