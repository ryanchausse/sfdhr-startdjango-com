# Generated by Django 3.2.8 on 2021-12-11 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0019_auto_20211207_1909'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='lenspackageitem',
            name='lens_package_only_one_of_three_lens_categories_allowed',
        ),
    ]
