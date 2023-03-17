# Generated by Django 4.1 on 2023-03-14 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0012_properties_propertyvaluepairs_values_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVariants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.productsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='VariantsProperties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_value_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.propertyvaluepairs')),
            ],
        ),
        migrations.RemoveField(
            model_name='laptops',
            name='product',
        ),
        migrations.RemoveField(
            model_name='variants',
            name='product',
        ),
        migrations.RemoveField(
            model_name='variants',
            name='product_variant',
        ),
        migrations.RemoveField(
            model_name='variants',
            name='property_value_pair',
        ),
        migrations.DeleteModel(
            name='CoffeTables',
        ),
        migrations.DeleteModel(
            name='Laptops',
        ),
        migrations.DeleteModel(
            name='Variants',
        ),
        migrations.AddField(
            model_name='productvariants',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.variantsproperties'),
        ),
    ]
