# Generated by Django 4.1.1 on 2023-02-01 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type_name', models.CharField(blank=True, max_length=300, null=True)),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Categories.categories')),
            ],
        ),
    ]
