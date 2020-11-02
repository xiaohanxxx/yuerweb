#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path

from . import views

urlpatterns = [
    path(r'areas/', views.Area.as_view(), name='get_areas'),
    path(r'hospitallist/', views.HospitalList.as_view(), name='hospitallist'),
    path(r'hospital/', views.Hospital.as_view(), name='hospital')
]