#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path

from . import views

urlpatterns = [
    path(r'', views.Index.as_view()),
    path(r'areas/', views.Area.as_view(), name='areas'),
    path(r'hospitallist/', views.HospitalList.as_view(), name='hospitallist'),
    path(r'hospitallv/', views.HospitalLv.as_view(), name='hospitallv'),
    path(r'hospitaltype/', views.HospitalType.as_view(), name='hospitaltype')
]