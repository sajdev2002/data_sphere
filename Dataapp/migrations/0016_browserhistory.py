# Generated by Django 5.1.6 on 2025-04-10 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dataapp', '0015_buss_data_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrowserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.URLField()),
                ('visited_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dataapp.user')),
            ],
        ),
    ]
