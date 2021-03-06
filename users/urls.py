#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path
from users import views

urlpatterns = [
    path('', views.center),
    path('upload', views.upload),
    path('register', views.register),
    path('login', views.userlogin),
    path('forget',views.forget),
    path('changepwd', views.changepwd),
    path('setusername',views.set_username),
    path('smsvif', views.smsvif),
    re_path(r'^centerhim/(\d+)', views.centerhim),  # 别人的个人中心
    path('centerMessage', views.centerMessage),  # 我的消息
    path(r'followapi', views.Followapi.as_view()),  # 关注功能接口

    path('notificate', views.getnoticate),

    path('outlogin', views.outlogin),
]
