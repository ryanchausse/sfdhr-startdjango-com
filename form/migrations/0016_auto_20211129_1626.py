# Generated by Django 3.2.8 on 2021-11-29 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0015_lenspackageitem_only_one_of_three_lens_categories_allowed'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='lenspackageitem',
            name='only_one_of_three_lens_categories_allowed',
        ),
        migrations.AddConstraint(
            model_name='lenspackageitem',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('lens_type__isnull', False), ('lens_material__isnull', True), ('lens_add_on__isnull', True)), models.Q(('lens_type__isnull', True), ('lens_material__isnull', False), ('lens_add_on__isnull', True)), models.Q(('lens_type__isnull', True), ('lens_material__isnull', True), ('lens_add_on__isnull', False)), _connector='OR'), name='only_one_of_three_lens_categories_allowed'),
        ),
    ]
