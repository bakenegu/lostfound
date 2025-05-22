from django.contrib import admin
from .models import UserProfile, LostItem, FoundItem
from .models import Match

admin.site.register(Match)
admin.site.register(UserProfile)
admin.site.register(LostItem)
admin.site.register(FoundItem)
