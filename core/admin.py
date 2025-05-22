from django.contrib import admin
from .models import UserProfile, LostItem, FoundItem

admin.site.register(UserProfile)
admin.site.register(LostItem)
admin.site.register(FoundItem)
