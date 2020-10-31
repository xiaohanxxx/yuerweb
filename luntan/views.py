import json

from django.shortcuts import render, HttpResponse, get_object_or_404
from django import views
from . import models

# Create your views here.

from django import forms
from django.core.paginator import Paginator


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5)
    content = forms.CharField(min_length=10)
    category_id = forms.IntegerField()


# get:获取帖子及评论， post: 发表帖子
class Article(views.View):
    def get(self, request, *args, **kwargs):
        aid = request.GET.get("id")
        # 获取帖子
        a_data = get_object_or_404(models.PostArtical, pk=aid)
        # 获取评论
        c_data = a_data.comment_set.all().values()
        return HttpResponse("这是帖子内容及评论:{}, 这是评论：{}".format(a_data, c_data))

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)
        if not form.is_valid():
            return HttpResponse("发表失败！！！！！！")

        data = form.cleaned_data
        data['author_id'] = request.session.get('user_id')

        # 自定义图片上传
        # new_img_path = handle_upload_file(request.FILES['head_img'],request)
        # 但是在views也保存了一份,我们给他改掉改成我们自己的就行了
        # form_data['head_img'] = new_img_path

        models.PostArtical.objects.create(**data)
        return HttpResponse("发表成功！！！！")


# post: 发表评论
class Comment(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "pinglun.html")

    def post(self, request, *args, **kwargs):
        user_id = request.session.get("user_id", 1)  # 暂时没有就先给1
        data = json.loads(request.body)
        data['user_id'] = user_id
        models.Comment.objects.create(**data)
        return HttpResponse("评论成功！！！！！！！！！！")


# 获取帖子列表
class ArticleIndex(views.View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get("category_id")
        curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
        pagi_data = models.PostArtical.objects.filter(category_id=category_id)
        paginator = Paginator(pagi_data, 10)
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

        return HttpResponse(
            "这是第{}页的数据，一共有{}页数据，页码列表是{}，本页数据内容是/r/n{}".format(
                curuent_page_num, pag_num, pag_range, paginator, curuent_page
            )
        )
