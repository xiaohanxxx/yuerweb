#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path

from . import views

urlpatterns = [
    path(r'', views.Index.as_view(), name="index"),
    path(r'postindex/', views.ToGroups.as_view(), name="postindex"),
    path(r'groups/', views.Groups.as_view(), name="groups"),
    path(r'topics/', views.Topics.as_view(), name="topics"),
    path(r'postinglist/', views.PostingList.as_view(), name="postinglist"),
    path(r'posting/', views.Posting.as_view(), name="posting"),
    path(r'comment/', views.Comment.as_view(), name="comment"),
]