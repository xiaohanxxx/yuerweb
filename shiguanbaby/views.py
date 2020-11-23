import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, HttpResponse, get_object_or_404
from django import views
from . import models


# Create your views here.
# 主界面
class Index(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sgyer.html')


class Areas(views.View):
    def get(self, request, *args, **kwargs):
        data = models.Areas.objects.all()
        res = [{"id": i.id, "name": i.name} for i in data]
        return HttpResponse(json.dumps({"data": res}), content_type="application/json")


class ArticlesList(views.View):
    def get(self, request, *args, **kwargs):
        aId = request.GET.get("aid")
        num = request.GET.get('num', 10)
        aObj = get_object_or_404(models.Areas, pk=aId)
        articleList = aObj.articles_set.all().order_by("publish_date")
        curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
        paginator = Paginator(articleList, num)
        pag_num = paginator.num_pages  # 获取整个表的总页数
        curuent_page = paginator.page(curuent_page_num)  # 获取当前页的数据
        if pag_num < 11:  # 判断当前页是否小于11个
            pag_range = paginator.page_range
        else:
            if curuent_page_num < 6:
                pag_range = range(1, 11)
            elif curuent_page_num > (paginator.num_pages) - 5:
                pag_range = range(pag_num - 9, pag_num + 1)
            else:
                pag_range = range(curuent_page_num - 5, curuent_page_num + 5)  # 当前页+5大于最大页数时

        res = {
            "curuent_page_num": curuent_page_num,  # 当前页数
            "page_num": pag_num,  # 总共页数
            "page_range": [i for i in pag_range],  # 页码列表
            "curuent_page": [
                {
                    "id": i.id,
                    "title": i.title,
                    "content": i.content,
                    "publish_date": str(i.publish_date),
                    "topics": i.topics,
                    "user": i.user,
                } for i in curuent_page
            ]
        }
        # if request.GET.get('all'):
        #     return render(request, 'sgyer.html', {"data": res})
        return HttpResponse(json.dumps({"data": res}), content_type="application/json")


# 获取文章
class Articles(views.View):
    def get(self, request, *args, **kwargs):
        articleId = request.GET.get('aid')
        artObj = get_object_or_404(models.Articles, pk=articleId)
        # 获取帖子发布人信息
        artData = {
            "id": artObj.id,
            "title": artObj.title,
            "content": artObj.content,
            "publish_date": str(artObj.publish_date),
            "topics": artObj.topics,
            "user": artObj.user,
        }
        return render(request, 'articles.html', {"data": artData})


# 获取热点标签
class HotTopics(views.View):
    def get(self, request, *args, **kwargs):
        num = request.GET.get("num", 6)
        hotData = models.Articles.objects.values('topics').annotate(count=Count('topics')).order_by("-count")[:int(num)]
        topicsList = models.Topics.objects.filter(id__in=[i['topics'] for i in hotData])
        topicsDic = {i.id: i.name for i in topicsList}
        res = []
        for i in hotData:
            i['name'] = topicsDic[i['topics']]
            res.append(i)
        return HttpResponse(json.dumps({"data": res}), content_type="application/json")



