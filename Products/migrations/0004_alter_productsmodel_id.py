# Generated by Django 4.1 on 2023-03-04 16:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0003_alter_productsmodel_brands'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsmodel',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
