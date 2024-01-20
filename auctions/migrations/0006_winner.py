# Generated by Django 5.0 on 2024-01-14 04:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_comment_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('win_item', models.ManyToManyField(related_name='win_items', to='auctions.auctionitem')),
                ('winner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='auctions.userprofile')),
            ],
        ),
    ]
