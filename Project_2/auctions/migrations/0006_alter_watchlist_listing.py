# Generated by Django 4.1.7 on 2023-07-20 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_watchlist_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
