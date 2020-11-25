from django.contrib import admin

from users.models import Userinfo, Follow


# Register your models here.
@admin.register(Userinfo)
class Bk_Admin(admin.ModelAdmin):
    list_display = ('user', 'user_avatar', 'phone', 'integral', 'level')
    list_per_page = 20
    search_fields = ['user__username','phone']
    list_filter = ['level']  # 关键字过滤


@admin.register(Follow)
class Bk_Admin(admin.ModelAdmin):
    list_display = ('follower', 'followed', 'date')
