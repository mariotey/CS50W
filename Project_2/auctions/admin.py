from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Listing, Bids, Comments

class ListAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "category", "start_bid", "creator")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListAdmin)
