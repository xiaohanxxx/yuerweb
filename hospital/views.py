import json

from django.shortcuts import render, get_object_or_404
from django import views
from . import models
from django.shortcuts import HttpResponse


# Create your views here.

# 获取范围
class Index(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'yiyuantuijian.html')

# 获取范围
class Area(views.View):
    def get(self, request, *args, **kwargs):
        data = models.Area.objects.all().values()
        return HttpResponse("国际范围有：{}".format(data))


# 获取指定范围医院
class HospitalList(views.View):
    def get(self, request, *args, **kwargs):
        chk = request.GET
        dict = {k: v for k, v in chk.items()}
        rData = models.Hospital.objects.filter(**dict)
        return HttpResponse("ok------{}".format(rData))


# 获取指定医院
class Hospital(views.View):
    def get(self, request, *args, **kwargs):
        hId = request.GET.get("hid")
        hData = get_object_or_404(models.Hospital, pk=hId)
        return HttpResponse("医院内容：{}".format(hData))


if __name__ == '__main__':
    # area测试数据
    worldarea = ["国内", "国外"]
    cityarea1 = ["武汉", "上海", "广州"]
    cityarea2 = ["美国", "新加坡", "印尼"]
    insertList = []
    for i in worldarea:
        worldObj = models.Area.objects.create(name=i)
        if i == "国内":
            for k in cityarea1:
                insertList.append(models.Area(name=k, parent=worldObj))
        if i == "国外":
            for k in cityarea2:
                insertList.append(models.Area(name=k, parent=worldObj))

    models.Area.objects.bulk_create(insertList)

    # 医院等级测试数据
    insert = []
    for i in ["一甲", "二甲", "三甲"]:
        insert.append(models.HospitalLv(name=i))
    models.HospitalLv.objects.bulk_create(insert)

    # 医院类型测试数据
    insert = []
    for i in ["试管", "不孕", "受精"]:
        insert.append(models.HospitalType(name=i))
    models.HospitalType.objects.bulk_create(insert)

    # 医院介绍
    cObj = models.Area.objects.get(name="武汉")
    pObj = cObj.parent
    wObj = pObj.parent
    lvObj = models.HospitalLv.objects.get(name="一甲")
    data = {
        "title": "武汉第一医院",
        "content": "武汉第一医院简介",
        "address": "武汉第一医院地址",
        "phone": "武汉第一医院电话",
        "worldarea": wObj,
        "privincearea": pObj,
        "cityarea": cObj,
        "hospitallv": lvObj
    }
    hObj = models.Hospital.objects.create(**data)
    tObj1 = models.HospitalType.objects.get(pk=1)
    tObj2 = models.HospitalType.objects.get(pk=2)
    hObj.hospitaltype.add(*[tObj1, tObj2])
    print("xxxxxxxxxxx")