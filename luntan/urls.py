#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path

from . import views

urlpatterns = [
    path(r'index/', views.ArticleIndex.as_view(), name='index'),
    path(r'tiezi/', views.Article.as_view(), name='tiezi'),
    path(r'pinglun/', views.Comment.as_view(), name='pinglun'),
]