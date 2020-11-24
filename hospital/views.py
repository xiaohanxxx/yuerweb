import json

from django.core.paginator import Paginator
from django.forms import model_to_dict
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


# 获取医院主页
class Hindex(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "yiyuanxiangqing.html")


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
        dict = {k: v for k, v in chk.items() if v and k not in ["num", "page"]}
        rData = models.Hospital.objects.filter(**dict)
        num = request.GET.get('num', 10)
        curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
        paginator = Paginator(rData, num)
        curuent_page = paginator.page(curuent_page_num)  # 获取当前页的数据
        resData = [
            {"id": i.id,
             "title": i.title,
             "content": i.content,
             "address": i.address,
             "phone": i.phone,
             "hospitallv": i.hospitallv.name,
             "doctornum": i.doctor_set.all().count()
             } for i in curuent_page
        ]
        return HttpResponse(json.dumps({"data": resData, "allnum": len(rData)}))


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
            "hospitaltype": [{"id": i.id, "name": i.name} for i in hData.hospitaltype.all()],
            "thumb": hData.thumb.url,
        }
        doctorList = []
        for i in hData.doctor_set.all():
            data = model_to_dict(i)
            data['thumb'] = data['thumb'].url
            data.update({"gender": i.get_gender_display()})
            del data['power']
            doctorList.append(data)
        resData['dictorlist'] = doctorList
        return HttpResponse(json.dumps({"data": resData}))


# 获取医生列表
class GetDoctorList(views.View):
    def get(self, request, *args, **kwargs):
        doctorObjList = models.Doctor.objects.all()
        num = request.GET.get('num', 10)
        curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
        paginator = Paginator(doctorObjList, num)
        curuent_page = paginator.page(curuent_page_num)  # 获取当前页的数据
        doctorList = []
        for i in curuent_page:
            resData = model_to_dict(i)
            resData['thumb'] = resData['thumb'].url
            resData['gender'] = i.get_gender_display()
            del resData['power']
            doctorList.append(resData)
        return HttpResponse(json.dumps({"data": doctorList, "allnum": len(doctorObjList)}))


# 获取指定医院医生
class GetDoctor(views.View):
    def get(self, request, *args, **kwargs):
        did = request.GET.get("did")
        dData = get_object_or_404(models.Doctor, pk=did)
        resData = model_to_dict(dData)
        resData['gender'] = dData.get_gender_display()
        resData['hospital'] = dData.hospital.title
        resData['thumb'] = resData['thumb'].url
        resData['mail'] = [model_to_dict(i) for i in dData.mail_set.all()]
        del resData['power']
        return render(request, 'yishengxiangqing.html', {"data": resData})
        # return HttpResponse(json.dumps({"data": resData}))


# 获取重要类型列表
class GetPowerList(views.View):
    def get(self, request, *args, **kwargs):
        typeListObj = models.Power.objects.all()
        res = [{"id": i.id, "name": i.name} for i in typeListObj]
        return HttpResponse(json.dumps({"data": res}))


# 指定重要类型的医院
class PowerHospital(views.View):
    def get(self, request, *args, **kwargs):
        type = request.GET.get("type")
        num = request.GET.get("num", 10)
        typeObj = get_object_or_404(models.Power, pk=type)
        artObjList = typeObj.hospital_set.all()[:int(num)]
        res = [
            {
                "id": i.id,
                "title": i.title,
                "content": i.content,
                "address": i.address,
                "phone": i.phone,
                "worldarea": i.worldarea.name,
                "privincearea": i.privincearea.name,
                "cityarea": i.cityarea.name,
                "hospitallv": i.hospitallv.name,
                "hospitaltype": i.hospitaltype.name,
                "thumb": i.thumb.url,
            } for i in artObjList
        ]
        return HttpResponse(json.dumps({"data": res}))


# 指定重要类型的医生
class PowerDoctor(views.View):
    def get(self, request, *args, **kwargs):
        type = request.GET.get("type")
        num = request.GET.get("num", 10)
        typeObj = get_object_or_404(models.Power, pk=type)
        artObjList = typeObj.doctor_set.all()[:int(num)]
        res = [
            {
                "id": i.id,
                "name": i.name,
                "gender": i.get_gender_display(),
                "area": i.area,
                "keshi": i.keshi,
                "zhiwei": i.zhiwei,
                "goodjob": i.goodjob,
                "title": i.title,
                "details": i.details,
                "thumb": i.thumb.url,
                "hospital": i.hospital.title
            } for i in artObjList
        ]
        return HttpResponse(json.dumps({"data": res}))
