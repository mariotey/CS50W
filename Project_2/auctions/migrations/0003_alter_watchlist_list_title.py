# Generated by Django 4.1.7 on 2023-07-20 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_watchlist_delete_bids_delete_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='list_title',
            field=models.CharField(max_length=64),
        ),
    ]
