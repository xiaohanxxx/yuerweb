from django.contrib import admin
from . import models


# Register your models here.
class CommentInline(admin.TabularInline):
    model = models.Comment


class PostingAdmin(admin.ModelAdmin):
    inlines = [CommentInline]  # Inline


admin.site.register(models.Posting, PostingAdmin)
admin.site.register([models.Groups, models.Topics])