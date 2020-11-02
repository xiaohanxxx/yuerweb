# from django import views
# from django.shortcuts import render, HttpResponse
# from . import models
# from django.shortcuts import get_object_or_404
#
# # Create your views here.
#
# """医院推荐"""
#
#
# # 查看医院推荐最上级目录
# class TuiJianRange(views.View):
#     def get(self, request, *args, **kwargs):
#         data = models.Area.objects.filter(parent_id=None)
#         return HttpResponse(data.values())
#
#
# # 查看指定医院的推荐文章
# class ChoiceRange(views.View):
#     def get(self, request, *args, **kwargs):
#         world = request.GET.get("w", 0)
#         city = request.GET.get("c", 0)
#         # 所有医院
#         if not world and not city:
#             data = models.ArticalType.objects.get(name="医院介绍")
#             artical_list = data.artical_set.all()
#             return HttpResponse("所有医院推荐文章：{}".format(artical_list))
#
#         # 国内或者国外所有医院
#         elif world and not city:
#             # 查找下属所有城市
#             w_data = get_object_or_404(models.Area, pk=world)
#             # 正向查找下属所有城市
#             c_data = w_data.area_set.all()
#             # 查找下属所有医院
#             h_list = []
#             for i in c_data:
#                 h_list.append(i.area_set.all())
#             # 查找医院所属医院介绍文章
#             a_list = []
#             for i in h_list:
#                 for k in i:
#                     a_data = k.artical_set.filter(artical_type__name="医院介绍")
#                     if not a_data:
#                         continue
#                     a_list.append(a_data)
#             return HttpResponse("指定国内外医院介绍文章：{}".format(a_list))
#
#         # 某个城市所有医院介绍
#         else:
#             c_data = get_object_or_404(models.Area, pk=city)
#             # 正向查找下属所有医院
#             h_data = c_data.area_set.all()
#             a_list = []
#             for i in h_data:
#                 a_data = i.artical_set.filter(artical_type__name="医院介绍")
#                 if not a_data:
#                     continue
#                 a_list.append(a_data)
#             return HttpResponse("指定城市医院介绍文章：{}".format(a_list))
#
#
# # 查看医院介绍文章
# class HospitalAritcal(views.View):
#     def get(self, request, *args, **kwargs):
#         aid = request.GET.get("id")
#         artical = models.Artical.objects.filter(pk=aid)
#         if not artical:
#             return HttpResponse("没有这篇文章！！！！！！")
#         return HttpResponse("医院介绍文章内容：{}".format(artical))
#
#
# """试管婴儿"""
#
#
# class ShiguanBaby(views.View):
#     def get(self, request, *args, **kwargs):
#         world = request.GET.get('w')
#         w_data = get_object_or_404(models.Area, pk=world)
#         a_data = w_data.artical_set.filter(artical_type__name="试管婴儿")
#         return HttpResponse("试管婴儿信息：{}".format(a_data))
#
#
# if __name__ == '__main__':
#     # 区域测试数据
#     data = {
#         "国内": ['武汉', '上海', '广州'],
#         "国外": ['美国', '英国', '俄罗斯']
#     }
#     for k, v in data.items():
#         world = models.Area.objects.create(name=k)
#         city_insert = []
#         for i in v:
#             city_insert.append(models.Area(name=i, parent_id=world.pk))
#         models.Area.objects.bulk_create(city_insert)
#
#         hospital_insert = []
#         for m in v:
#             data = models.Area.objects.get(name=m)
#             for n in range(1, 3):
#                 hospital_insert.append(models.Area(name=m + '医院' + str(n), parent_id=data.pk))
#         models.Area.objects.bulk_create(hospital_insert)
#
#     # 文章类型测试数据
#     artical_type_insert = []
#     for i in ['医院介绍', '备孕', '怀孕', '育儿', '试管婴儿', '不孕不育']:
#         artical_type_insert.append(models.ArticalType(name=i))
#     models.ArticalType.objects.bulk_create(artical_type_insert)
#
#     # 文章测试数据
#     # 查询所有最子级医院
#     data = models.Area.objects.filter(parent_id__isnull=True).values_list('id', flat=True)
#     data = models.Area.objects.filter(parent_id__in=data).values_list('id', flat=True)
#     data = models.Area.objects.filter(parent_id__in=data)
#     # 为所有最子集医院添加类型对应文章
#     t_data = models.ArticalType.objects.all()
#     for i in t_data:  # 文章类型
#         for k in data:  # 子级医院
#             title = str(k.name) + str(i.name) + '文章标题'
#             content = str(k.name) + str(i.name) + '文章内容'
#             artical = models.Artical.objects.create(title=title, content=content, area_id=k.pk)
#             artical.artical_type.add(i)
#
#     # 删除文章
#     data = models.Artical(pk=2)
#     data.delete()
