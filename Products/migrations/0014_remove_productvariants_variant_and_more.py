# Generated by Django 4.1 on 2023-03-14 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0013_productvariants_variantsproperties_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariants',
            name='variant',
        ),
        migrations.AddField(
            model_name='productvariants',
            name='property',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Products.properties'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productvariants',
            name='variant_id',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='VariantsProperties',
        ),
    ]
