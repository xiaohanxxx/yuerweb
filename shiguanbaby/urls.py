#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path

from . import views

urlpatterns = [
    path(r"areas/", views.Areas.as_view(), name="areas"),
    path(r"articleslist/", views.ArticlesList.as_view(), name="articleslist"),
]