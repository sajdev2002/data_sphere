# Generated by Django 5.1.6 on 2025-04-14 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dataapp', '0029_productopinion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productopinion',
            old_name='submitted_by',
            new_name='login',
        ),
    ]
