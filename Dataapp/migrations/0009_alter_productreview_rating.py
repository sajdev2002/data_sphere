# Generated by Django 5.1.6 on 2025-04-06 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dataapp', '0008_productreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)]),
        ),
    ]
