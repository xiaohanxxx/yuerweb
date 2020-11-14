from django.contrib import admin
from baike.models import Bk_menu, Child_menu, Artical
from django import forms


# Register your models here.


@admin.register(Bk_menu)
class Bk_Admin(admin.ModelAdmin):
    list_display = ('menu_name', 'is_active')


@admin.register(Child_menu)
class Child_Admin(admin.ModelAdmin):
    list_display = ('menu_name', 'relation', 'is_active')




@admin.register(Artical)
class Artical_Admin(admin.ModelAdmin):
    list_display = ('title','thumb', 'category', 'author', 'excerpt', 'click_count')
    # readonly_fields = ("excerpt", "click_count",)
    list_per_page = 10

