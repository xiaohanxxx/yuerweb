from django.shortcuts import render
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
        request.POST.get('type') # 首页1，论坛2，百科3
        banner_list = [i for i in models.Banner.objects.all().values()]
    banners = function(banner_list)
    print(banners)