# Generated by Django 3.2.8 on 2022-05-19 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0055_normform_preview'),
    ]

    operations = [
        migrations.AddField(
            model_name='normform',
            name='emailed',
            field=models.BooleanField(default=False),
        ),
    ]
