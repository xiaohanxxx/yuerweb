from django.shortcuts import render, HttpResponse, get_object_or_404
from django import views
from . import models


# Create your views here.
class Areas(views.View):
    def get(self, request, *args, **kwargs):
        data = models.Areas.objects.all()
        return HttpResponse("范围标签有：{}".format(data))


class ArticlesList(views.View):
    def get(self, request, *args, **kwargs):
        aId = request.GET.get("aid")
        aObj = get_object_or_404(models.Areas, pk=aId)
        articlesList = aObj.articles_set.all().order_by("publish_date")
        return HttpResponse("文章列表:{}".format(articlesList))

