# Generated by Django 4.1 on 2023-03-13 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0011_alter_productsmodel_variations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyValuePairs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.properties')),
            ],
        ),
        migrations.CreateModel(
            name='Values',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_name', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='productsmodel',
            name='variations',
        ),
        migrations.CreateModel(
            name='Variants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='Products.productsmodel')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_variant', to='Products.productsmodel')),
                ('property_value_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.propertyvaluepairs')),
            ],
        ),
        migrations.AddField(
            model_name='propertyvaluepairs',
            name='value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.values'),
        ),
        migrations.CreateModel(
            name='ProductProperties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.productsmodel')),
                ('property_value_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.propertyvaluepairs')),
            ],
        ),
    ]