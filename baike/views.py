from django.shortcuts import render, HttpResponse
from baike import models
from django.core import serializers
from django.http import JsonResponse
import json


# Create your views here.

def baike(request):
    return render(request, 'baike.html')


# 获取栏目api
def baikemenu(request):
    if request.method == 'POST':
        type = request.GET.get('type')
        code = 200
        msg = '成功'
        if int(type) == 1:
            menu = models.Bk_menu.objects.all().values()
        elif int(type) == 2:
            menu = models.Child_menu.objects.all().values()
        elif int(type) == 3:
            menu = models.Menu.objects.all().values()
        else:
            code = 400
            msg = '接口错误'
            menu = list()

        data = {
            'code': code,
            'msg': msg,
            'menu': list(menu)
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


# 获取三级栏目api
def sjld(request):
    menu_one = models.Bk_menu.objects.all()
    data = []
    for i in menu_one:
        child = i.child_menu_set.all()
        for j in child:
            menu = j.menu_set.all()
            data.append(
                {
                    'id': i.id,
                    'menu_name': i.menu_name,
                    'type': 1,
                    'children': [
                        {
                            'id': j.id,
                            'menu_name': j.child_name,
                            'type': 2,
                            'children': [{"id": i.id, "menu_name": i.child_name, 'type': 3} for i in menu]
                        }
                    ],
                }
            )

    return HttpResponse(json.dumps(data), content_type="application/json")


# 获取文章
def artcle(request):
    if request.method == 'GET':
        menu_id = request.GET.get('menu_id')
        page = request.GET.get('page')
        rows = request.GET.get('rows')
        menu = models.Menu.objects.get(id=menu_id)
        artcle_list = menu.artical_set.values()







from django.views import View
from rest_framework.views import APIView


# CBV
class OrderView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('获取订单')

    def post(self, request, *args, **kwargs):
        return HttpResponse('创建订单')

    def put(self, request, *args, **kwargs):
        return HttpResponse('修改订单')

    def delete(self, request, *args, **kwargs):
        return HttpResponse('删除订单')
