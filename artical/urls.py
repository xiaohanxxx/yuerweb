#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path

from . import views

urlpatterns = [
    path(r'tuijianrange/', views.TuiJianRange.as_view()),
    path(r'choicetuijian/', views.ChoiceRange.as_view()),
    path(r'hospitalartical/', views.HospitalAritcal.as_view()),
    path(r'shiguanbaby/', views.ShiguanBaby.as_view()),
]