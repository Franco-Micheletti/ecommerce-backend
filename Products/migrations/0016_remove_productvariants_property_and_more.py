# Generated by Django 4.1 on 2023-03-15 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0015_productvariants_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariants',
            name='property',
        ),
        migrations.RemoveField(
            model_name='productvariants',
            name='value',
        ),
        migrations.AddField(
            model_name='productvariants',
            name='values',
            field=models.TextField(blank=True, null=True),
        ),
    ]
