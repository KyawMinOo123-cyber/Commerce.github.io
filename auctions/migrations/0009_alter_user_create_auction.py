# Generated by Django 5.0 on 2024-01-17 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_user_create_auction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='create_auction',
            field=models.BooleanField(default=True),
        ),
    ]
