# Generated by Django 3.2.8 on 2022-03-03 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0036_alter_normform_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normform',
            name='date',
            field=models.DateField(blank=True),
        ),
    ]
