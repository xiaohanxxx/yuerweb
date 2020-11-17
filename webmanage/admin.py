from django.contrib import admin
from webmanage.models import FriendLink

# Register your models here.
@admin.register(FriendLink)
class Friend_link(admin.ModelAdmin):
    list_display = ('link_name','idx', 'link')
