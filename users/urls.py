#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path
from . import views

urlpatterns = [
    path(r'login/', views.Login.as_view(), name='login'),
    path(r'register/', views.Register.as_view(), name='register'),
    path(r'loginout/', views.LoginOut.as_view(), name='loginout'),
]