# Generated by Django 4.1.7 on 2023-07-20 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_watchlist_list_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='list_title',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listing',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
            preserve_default=False,
        ),
    ]
