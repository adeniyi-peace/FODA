# Generated by Django 5.2.3 on 2025-07-17 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_address_phone_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='old_cart',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
