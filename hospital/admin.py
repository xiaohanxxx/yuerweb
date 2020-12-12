from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Area)
class Area_Admin(admin.ModelAdmin):
    list_display = ('name', 'parent',)


@admin.register(models.HospitalLv)
class HospitalLv_Admin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.HospitalType)
class HospitalType_Admin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Power)
class Power_Admin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.ImageUp)
class ImageUp_Admin(admin.ModelAdmin):
    list_display = ('image',)


@admin.register(models.Hospital)
class Hospital_Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'hospitallv',)
    search_fields = ('title',)
    list_filter = ('hospitallv',)
    list_per_page = 10


@admin.register(models.Mail)
class Mail_Admin(admin.ModelAdmin):
    list_display = ('id', 'username', 'doctor',)


@admin.register(models.Doctor)
class Doctor_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hospital', 'gender',)
    search_fields = ('name',)
    list_filter = ('hospital',)

# admin.site.register(
#     [models.Area, models.Hospital, models.HospitalLv, models.HospitalType, models.Doctor, models.Mail, models.Power,
#      models.ImageUp], Admin)
