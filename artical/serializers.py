#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# !/usr/bin/env python
# _*_ coding:utf-8 _*_
from rest_framework import serializers
from . import models


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Area
        fields = (
            'id',
            'name'
        )


class ArticalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticalType
        fields = (
            'id',
            'name'
        )


class ArticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artical
        fields = (
            'id',
            'title',
            'content',
            'create_time',
            'area',
            'artical_type',
        )
