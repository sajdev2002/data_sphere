# Generated by Django 5.1.6 on 2025-04-13 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dataapp', '0025_remove_educationdetail_file_employeedetails_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationdetail',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='education_files/'),
        ),
    ]
