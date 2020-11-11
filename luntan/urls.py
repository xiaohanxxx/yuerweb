#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path

from . import views

urlpatterns = [
    path(r'', views.Luntan.as_view()),
    path(r'areas/', views.Areas.as_view(), name='areas'),
    path(r'topics/', views.Topics.as_view(), name='topices'),
    path(r'articlelist/', views.ArticlesList.as_view(), name='articlelist'),
    path(r'articles/', views.Article.as_view(), name='articles'),
    path(r'comment/', views.Comment.as_view(), name='comment'),
    path(r'hotarticles/', views.HotAritcles.as_view(), name='hotarticles'),
    # path(r'imageup/', views.ImageUp.as_view(), name='imageup'),
]