# Generated by Django 5.0.3 on 2024-05-09 15:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script_generator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scriptslist',
            name='generatedSummary',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
