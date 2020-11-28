from django.contrib import admin
from webmanage.models import FriendLink,Banner,BaikeBanner,YuerBanner

# Register your models here.
@admin.register(FriendLink)
class Friend_link(admin.ModelAdmin):
    list_display = ('link_name','idx', 'link')

@admin.register(Banner)
class Index_Banner_Admin(admin.ModelAdmin):
    list_display = ('title', 'idx', 'cover', 'image_img', 'is_active', 'add_time')

@admin.register(BaikeBanner)
class Baike_Banner_Admin(admin.ModelAdmin):
    list_display = ('title', 'idx', 'cover', 'image_img', 'is_active', 'add_time')

@admin.register(YuerBanner)
class Luntan_Banner_Admin(admin.ModelAdmin):
    list_display = ('title', 'idx', 'cover', 'image_img', 'is_active', 'add_time')
