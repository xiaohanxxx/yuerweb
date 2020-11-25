#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.urls import re_path, path

from . import views

urlpatterns = [
    path(r'', views.Index.as_view(), name="index"),
    path(r'postindex/', views.ToGroups.as_view(), name="postindex"),
    path(r'groups/', views.Groups.as_view(), name="groups"),
    path(r'grouplist/', views.GroupList.as_view(), name="grouplist"),
    path(r'topics/', views.Topics.as_view(), name="topics"),
    path(r'postinglist/', views.PostingList.as_view(), name="postinglist"),
    path(r'posting/', views.Posting.as_view(), name="posting"),
    path(r'comment/', views.Comment.as_view(), name="comment"),
    path(r'toposting/', views.ToPosting.as_view(), name="toposting"),
    path(r'topost/', views.ToPost.as_view(), name="topost"),
    path(r'hottopics/', views.HotTopics.as_view(), name="hottopics"),
    path(r'hotarticles/', views.HotArticles.as_view(), name="hotarticles"),
    path(r'thumbup/', views.ThumbUp.as_view(), name="thumbup")
]