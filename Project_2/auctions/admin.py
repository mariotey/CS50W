""" Tells the Django's admin app how to manipulate databases """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Listing, Bid, WatchList

# Customizes how Admin App displays your models
class ListAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "category", "bid_value", "creator")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListAdmin)
admin.site.register(Bid)
admin.site.register(WatchList)
