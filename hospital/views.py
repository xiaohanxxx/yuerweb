import json

from django.shortcuts import render, get_object_or_404
from django import views
from . import models
from django.shortcuts import HttpResponse


# Create your views here.

# 获取医院推荐主页
class Index(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "yiyuantuijian.html")


# 获取范围
class Area(views.View):
    def get(self, request, *args, **kwargs):
        data = models.Area.objects.all()
        resData = [{"id": i.id, "name": i.name, "parent_id": i.parent_id} for i in data]
        return HttpResponse(json.dumps({"data": resData}))


# 获取指定范围医院
class HospitalList(views.View):
    def get(self, request, *args, **kwargs):
        chk = request.GET
        dict = {k: v for k, v in chk.items()}
        rData = models.Hospital.objects.filter(**dict)
        resData = [{"id": i.id, "title": i.title, "content": i.content, "address": i.address} for i in rData]
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

