# Generated by Django 4.1 on 2023-03-15 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0017_productsmodel_variant_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsmodel',
            name='variant_options',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
