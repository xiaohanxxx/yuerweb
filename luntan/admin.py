from django.contrib import admin
from . import models


# Register your models here.
# class CommentInline(admin.TabularInline):
    # model = models.Comment


# class ArticlesAdmin(admin.ModelAdmin):
#     inlines = [CommentInline]  # Inline


# admin.site.register(models.Articles, ArticlesAdmin)
admin.site.register([models.Areas, models.Articles, models.ThumbUp, models.Comment, models.Topics])