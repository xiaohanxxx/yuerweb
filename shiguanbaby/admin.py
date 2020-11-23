from django.contrib import admin

# Register your models here.
from shiguanbaby import models


class ArticleTypeAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id', '__str__')


admin.site.register([models.Areas, models.Articles, models.Topics, models.ArticleType], ArticleTypeAdmin)
