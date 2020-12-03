#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from haystack import indexes
from .models import *


class HospitalIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Hospital

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class DoctorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Doctor

    def index_queryset(self, using=None):
        return self.get_model().objects.all()