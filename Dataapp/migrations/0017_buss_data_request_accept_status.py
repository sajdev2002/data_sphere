# Generated by Django 5.1.6 on 2025-04-11 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dataapp', '0016_browserhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='buss_data_request',
            name='accept_status',
            field=models.IntegerField(default=0),
        ),
    ]
