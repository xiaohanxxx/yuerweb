from django.contrib import admin

# Register your models here.
from shiguanbaby import models

admin.site.register([models.Areas, models.Articles, models.Topics])