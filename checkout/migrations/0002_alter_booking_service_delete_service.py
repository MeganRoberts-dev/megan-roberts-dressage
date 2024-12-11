# Generated by Django 5.1.4 on 2024-12-11 09:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service'),
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]
