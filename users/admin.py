from django.contrib import admin
from users.models import Userinfo
from django.contrib.auth.models import User

# Register your models here.
@admin.register(Userinfo)
class Bk_Admin(admin.ModelAdmin):
    list_display = ('user', 'user_avatar', 'phone')