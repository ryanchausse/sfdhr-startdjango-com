# Generated by Django 3.2.8 on 2022-08-22 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0059_alter_physician_facility'),
    ]

    operations = [
        migrations.RenameField(
            model_name='physician',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='physician',
            name='facility',
        ),
        migrations.RemoveField(
            model_name='physician',
            name='last_name',
        ),
    ]
