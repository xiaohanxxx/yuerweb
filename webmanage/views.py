from django.shortcuts import render,HttpResponse
import json
from webmanage import models
# Create your views here.


def function(demo_list):
    demos = list()
    for i in range(len(demo_list)):
        if demo_list[i]['is_active'] == False:
            pass
        else:
            demos.append(demo_list[i])
    demos = sorted(demos, key=lambda e: e['idx'], reverse=False)
    return demos


def banner(request):
    if request.method == "POST":
        bannertype = request.POST.get('bannertype') # 首页1，论坛2，百科3
        if bannertype == "1":
            banner_list = [i for i in models.Banner.objects.all().values('id','idx','title','cover','is_active')]
        elif bannertype == "2":
            banner_list = [i for i in models.YuerBanner.objects.all().values('id','idx','title','cover','is_active')]
        elif bannertype == "3":
            banner_list = [i for i in models.BaikeBanner.objects.all().values('id','idx','title','cover','is_active')]
        else:
            banner_list = list()
        banners = function(banner_list)
        data = {
            'code':200,
            'msg':'成功',
            'data':banners
        }
        return HttpResponse(json.dumps(data),content_type="application/json")