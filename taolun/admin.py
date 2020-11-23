from django.contrib import admin
from . import models


# Register your models here.
admin.site.register([models.Groups, models.Topics, models.Posting, models.Comment])