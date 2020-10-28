#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from rest_framework import serializers
from rest_framework import serializers
from . import models


class BaikeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaikeArea
        fields = (
            'id',
            'name',
            'parent'
        )


class ArticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaikeArtical
        fields = (
            'id',
            'title',
            'content',
            'ctime',
            'parent'
        )