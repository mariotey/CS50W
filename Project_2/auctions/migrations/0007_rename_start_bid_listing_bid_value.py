# Generated by Django 4.1.7 on 2023-07-20 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_bidder_name_bid_bidder_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='start_bid',
            new_name='bid_value',
        ),
    ]
