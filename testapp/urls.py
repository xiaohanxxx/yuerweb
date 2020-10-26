#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import path

from testapp import views

urlpatterns = [
    path('index/', views.Login.as_view()),
]
