from django.contrib import admin
from . import models


@admin.register(models.Areas)
class Areas_Admin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(models.Topics)
class Topics_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'area',)
    list_filter = ('area',)


@admin.register(models.Articles)
class Articles_Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user',)
    list_filter = ('user',)
    search_fields = ('title',)


@admin.register(models.Comment)
class Comment_Admin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'parent')
    list_filter = ('user', 'parent', )
    search_fields = ('comment',)


@admin.register(models.ThumbUp)
class ThumbUp_Admin(admin.ModelAdmin):
    list_display = ('id', 'articles', 'user',)
    list_filter = ('user',)
    search_fields = ('articles',)



# admin.site.register([models.Areas, models.Articles, models.ThumbUp, models.Comment, models.Topics])
