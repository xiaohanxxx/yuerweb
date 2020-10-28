#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from rest_framework import serializers
from rest_framework import serializers
from . import models


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Area
        fields = (
            'id',
            'name',
            'parent'
        )


class ArticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artical
        fields = (
            'id',
            'title',
            'content',
            'ctime',
            'parent'
        )