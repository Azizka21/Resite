# Generated by Django 5.1.4 on 2025-01-22 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_list_shuffled_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='templates',
            field=models.TextField(default='popa'),
        ),
    ]
