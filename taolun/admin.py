from django.contrib import admin
from . import models

class Admin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id', '__str__',)

# Register your models here.
admin.site.register([models.Groups, models.Topics, models.Posting, models.Comment, models.ThumbUpArticle, models.ThumbUpComment],Admin)