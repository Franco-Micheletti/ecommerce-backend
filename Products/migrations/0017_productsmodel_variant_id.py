# Generated by Django 4.1 on 2023-03-15 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0016_remove_productvariants_property_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsmodel',
            name='variant_id',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]