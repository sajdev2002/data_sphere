# Generated by Django 5.1.6 on 2025-04-06 14:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dataapp', '0011_employeedetails_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeedetails',
            name='company_name',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AddField(
            model_name='employeedetails',
            name='salary',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='employeedetails',
            name='login',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Dataapp.user'),
        ),
    ]
