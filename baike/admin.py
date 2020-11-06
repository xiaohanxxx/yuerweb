from django.contrib import admin
from baike.models import Bk_menu, Child_menu, Menu, Artical
from django import forms


# Register your models here.


@admin.register(Bk_menu)
class Bk_Admin(admin.ModelAdmin):
    list_display = ('menu_name', 'idx', 'is_active')


@admin.register(Child_menu)
class Child_Admin(admin.ModelAdmin):
    list_display = ('child_name', 'relation', 'idx', 'is_active')


@admin.register(Menu)
class Menu_Admin(admin.ModelAdmin):
    list_display = ('child_name', 'relation', 'idx', 'is_active')


@admin.register(Artical)
class Artical_Admin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'content', 'excerpt', 'click_count')
    readonly_fields = ("excerpt", "click_count",)


