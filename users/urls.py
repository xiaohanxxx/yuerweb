#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path
from users import views

urlpatterns = [

    path('register', views.register),
    path('login',views.login),

    path('outlogin', views.outlogin),
]