# Generated by Django 4.1 on 2023-03-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0009_productsmodel_variations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsmodel',
            name='variations',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
