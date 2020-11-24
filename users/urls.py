#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path
from users import views

urlpatterns = [
    path('', views.center),
    path('register', views.register),
    path('login', views.userlogin),
    path('changepwd', views.changepwd),
    path('smsvif', views.smsvif),
    path('centerhim',views.centerhim), # 别人的个人中心
    path('centerMessage',views.centerMessage), # 自己的个人中心


    path('outlogin', views.outlogin),
]
