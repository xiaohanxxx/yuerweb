from django.contrib import admin
from . import models


@admin.register(models.Groups)
class Groups_Admin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(models.Topics)
class Groups_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'area',)


@admin.register(models.Posting)
class Posting_Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user',)
    list_filter = ('user',)
    search_fields = ('title',)


@admin.register(models.Comment)
class Comment_Admin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'articles', 'user',)
    list_filter = ('user',)


@admin.register(models.ThumbUpArticle)
class ThumbUpArticle_Admin(admin.ModelAdmin):
    list_display = ('id', 'posting', 'user',)
    list_filter = ('user',)


@admin.register(models.ThumbUpComment)
class ThumbUpComment_Admin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user',)
    list_filter = ('user',)




# class Admin(admin.ModelAdmin):
#     # 需要显示的字段信息
#     list_display = ('id', '__str__',)
#
# # Register your models here.
# admin.site.register([models.Groups, models.Topics, models.Posting, models.Comment, models.ThumbUpArticle, models.ThumbUpComment],Admin)