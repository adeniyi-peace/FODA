# Generated by Django 5.2.1 on 2025-06-12 19:42

import sorl.thumbnail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='foods/'),
        ),
    ]
