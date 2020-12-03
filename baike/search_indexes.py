#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from haystack import indexes
from .models import *


class ArticalIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')

    def get_model(self):
        return Artical

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

