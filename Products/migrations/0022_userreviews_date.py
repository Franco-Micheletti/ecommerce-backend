# Generated by Django 4.1 on 2023-03-28 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0021_userreviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreviews',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
