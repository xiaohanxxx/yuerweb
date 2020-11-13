#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path

from . import views

urlpatterns = [
    path(r"", views.Index.as_view(), name="index"),
    path(r"areas/", views.Areas.as_view(), name="areas"),
    path(r"articleslist/", views.ArticlesList.as_view(), name="articleslist"),
    path(r"articles/", views.Articles.as_view(), name="article"),
    path(r"hottopics/", views.HotTopics.as_view(), name="hottopics"),
]