# Generated by Django 3.2.8 on 2022-04-15 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0047_icd10codes'),
    ]

    operations = [
        migrations.AddField(
            model_name='normform',
            name='mental_capacity',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='normform',
            name='placement_issues',
            field=models.BooleanField(default=False),
        ),
    ]
