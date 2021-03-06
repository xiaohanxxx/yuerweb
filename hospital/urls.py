#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path

from . import views

urlpatterns = [
    path(r'', views.Index.as_view()),
    path(r'areas/', views.Area.as_view(), name='areas'),
    path(r'hospitallist/', views.HospitalList.as_view(), name='hospitallist'),
    path(r'hospital/', views.Hospital.as_view(), name='hospital'),
    path(r'hospitallv/', views.HospitalLv.as_view(), name='hospitallv'),
    path(r'hospitaltype/', views.HospitalType.as_view(), name='hospitaltype'),
    path(r'doctorlist/', views.GetDoctorList.as_view(), name='doctorlist'),
    path(r'doctor/', views.GetDoctor.as_view(), name='doctor'),
    path(r'hindex/', views.Hindex.as_view(), name='hindex'),
    path(r'powerlist/', views.GetPowerList.as_view(), name='powerlist'),
    path(r'powerhospital/', views.PowerHospital.as_view(), name='powerhospital'),
    path(r'powerdoctor/', views.PowerDoctor.as_view(), name='powerdoctor')
]