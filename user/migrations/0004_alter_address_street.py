# Generated by Django 5.2.3 on 2025-07-02 21:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_address_options_address_street_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
