# Generated by Django 3.2.8 on 2022-03-07 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0040_alter_normform_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='normform',
            name='filename',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
