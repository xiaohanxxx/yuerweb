from django.contrib import admin
from . import models


# Register your models here.
admin.site.register([models.Area, models.Hospital, models.HospitalLv, models.HospitalType])