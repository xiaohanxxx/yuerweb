import json
from django import views
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from . import models
from . import serializers


# Create your views here.


class Artical(views.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("ok!!!!!")


if __name__ == '__main__':
    # 区域测试数据
    data = {
        "国内": ['武汉', '上海', '广州'],
        "国外": ['美国', '英国', '俄罗斯']
    }
    for k, v in data.items():
        world = models.Area.objects.create(name=k)
        city_insert = []
        for i in v:
            city_insert.append(models.Area(name=i, parent_id=world.pk))
        models.Area.objects.bulk_create(city_insert)

        hospital_insert = []
        for m in v:
            data = models.Area.objects.get(name=m)
            for n in range(1, 3):
                hospital_insert.append(models.Area(name=m + '医院' + str(n), parent_id=data.pk))
        models.Area.objects.bulk_create(hospital_insert)

    # 文章类型测试数据
    artical_type_insert = []
    for i in ['医院介绍', '备孕', '怀孕', '育儿', '试管婴儿', '不孕不育']:
        artical_type_insert.append(models.ArticalType(name=i))
    models.ArticalType.objects.bulk_create(artical_type_insert)

    # 文章测试数据
    # 查询所有最子级医院
    data = models.Area.objects.filter(parent_id__isnull=True).values_list('id', flat=True)
    data = models.Area.objects.filter(parent_id__in=data).values_list('id', flat=True)
    data = models.Area.objects.filter(parent_id__in=data)
    # 为所有最子集医院添加类型对应文章
    t_data = models.ArticalType.objects.all()
    for i in t_data:  # 文章类型
        for k in data:  # 子级医院
            title = str(k.name) + str(i.name) + '文章标题'
            content = str(k.name) + str(i.name) + '文章内容'
            artical = models.Artical.objects.create(title=title, content=content, area_id=k.pk)
            artical.artical_type.add(i)

    # 删除文章
    data = models.Artical(pk=2)
    data.delete()
