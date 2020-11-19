import json

from django.shortcuts import render, get_object_or_404
from django import views
from . import models
from django.shortcuts import HttpResponse


# Create your views here.

def xTree(data):
    resData = []
    for i in data:
        parent = {"id": i.id, "name": i.name, "child": []}
        hChild = i.area_set.all().count()
        if hChild:
            parent['child'] = xTree(i.area_set.all())
        resData.append(parent)
    return resData


# 获取医院推荐主页
class Index(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "yiyuantuijian.html")


# 获取范围
class Area(views.View):
    def get(self, request, *args, **kwargs):
        data = models.Area.objects.filter(parent_id=None)
        resData = xTree(data)
        # resData = [{"id": i.id, "name": i.name, "parent_id": i.parent_id} for i in data]
        return HttpResponse(json.dumps({"data": resData}))


# 获取指定范围医院
class HospitalList(views.View):
    def get(self, request, *args, **kwargs):
        chk = request.GET
        dict = {k: v for k, v in chk.items() if v}
        rData = models.Hospital.objects.filter(**dict)
        resData = [
            {"id": i.id,
             "title": i.title,
             "content": i.content,
             "address": i.address,
             "phone": i.phone,
             # TODO 获取医院医生人数
             "doctornum": 10
             } for i in rData
        ]
        return HttpResponse(json.dumps({"data": resData}))


# 获取医院等级
class HospitalLv(views.View):
    def get(self, request, *args, **kwargs):
        rData = models.HospitalLv.objects.all()
        resData = [{"id": i.id, "name": i.name} for i in rData]
        return HttpResponse(json.dumps({"data": resData}))


# 医院方向
class HospitalType(views.View):
    def get(self, request, *args, **kwargs):
        rData = models.HospitalType.objects.all()
        resData = [{"id": i.id, "name": i.name} for i in rData]
        return HttpResponse(json.dumps({"data": resData}))


# 获取指定医院
class Hospital(views.View):
    def get(self, request, *args, **kwargs):
        hId = request.GET.get("hid")
        hData = get_object_or_404(models.Hospital, pk=hId)
        resData = {
            "id": hData.id,
            "title": hData.title,
            "content": hData.content,
            "phone": hData.phone,
            "create_time": str(hData.create_time),
            "worldarea": hData.worldarea.name,
            "cityarea": hData.cityarea.name,
            "hospitallv": hData.hospitallv.name,
            "hospitaltype": hData.hospitaltype.name,
        }
        return HttpResponse(json.dumps({"data": resData}))

