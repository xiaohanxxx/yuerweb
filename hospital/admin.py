from django.contrib import admin
from . import models


# Register your models here.

class Admin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id', '__str__',)


admin.site.register([models.Area, models.Hospital, models.HospitalLv, models.HospitalType, models.Doctor, models.Mail, models.Power, models.ImageUp], Admin)
