#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import path, re_path
from django.conf.urls import url

from .views import BaikeArea, BaikeArtical

urlpatterns = [
    path(r'baikearea/', BaikeArea.as_view()),
    re_path(r'baikeartical/', BaikeArtical.as_view()),
]