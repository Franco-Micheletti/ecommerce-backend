# Generated by Django 4.1 on 2023-03-16 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0018_productsmodel_variant_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariants',
            name='values',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
