# Generated by Django 4.1 on 2023-03-09 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0007_rename_container_energydrinks_flavor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsmodel',
            name='quantity',
            field=models.SmallIntegerField(blank=True, default=1, null=True),
        ),
    ]
