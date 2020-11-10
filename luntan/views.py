import json

from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, get_object_or_404
from django import views
from . import models as luntanmodel
from . import form


# Create your views here.


# def xTree(data):
#     print(data)
#     resData = []
#     for i in data:
#         print(i)
#         chk = {"id": i.id, "name": i.name, "child": []}
#         if i.areas_topics.all():
#             chk['child'] = xTree(i.areas_topics.all())
#         resData.append(resData)
#     return resData


# 论坛主界面
class Luntan(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'yuerlt.html')


# 获取交流圈
class Areas(views.View):
    def get(self, request, *args, **kwargs):
        areasObjList = luntanmodel.Areas.objects.all()
        res = [{"id": i.id, "name": i.name,
                "child": [{"id": k.id, "name": k.name, "child": []} for k in i.areas_topics.all()]} for i in
               areasObjList]
        return HttpResponse(json.dumps({"data": res}), content_type="application/json")


# 获取分类话题
class Topics(views.View):
    def get(self, request, *args, **kwargs):
        areaId = request.GET.get('aid')
        areaObj = get_object_or_404(luntanmodel.Areas, pk=areaId)
        topics = areaObj.areas_topics.all()
        areaData = [{"id": i.id, "name": i.name} for i in topics]
        return HttpResponse(json.dumps({"data": areaData}), content_type="application/json")


# 获取分类帖子列表
class ArticlesList(views.View):
    def get(self, request, *args, **kwargs):
        topicsId = request.GET.get('tid')
        topicsData = luntanmodel.Topics.objects.get(pk=int(topicsId))
        articleList = topicsData.articles_set.exclude(isdelete=1).order_by("update_date")
        curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
        paginator = Paginator(articleList, 10)
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
                    "user": {"id": i.user.id, "username": i.user.username}
                } for i in curuent_page
            ]
        }

        return HttpResponse(json.dumps({"data": res}), content_type="application/json")


# 获取帖子
class Article(views.View):
    def get(self, request, *args, **kwargs):
        articleId = request.GET.get('aid')
        artObj = get_object_or_404(luntanmodel.Articles, pk=articleId)
        # 获取帖子评论信息
        commentData = artObj.articles_comment.all()
        # 获取帖子发布人信息
        artData = {
            "id": artObj.id,
            "title": artObj.title,
            "content": artObj.content,
            "publish_date": str(artObj.publish_date),
            "user": {"id": artObj.user.id, "username": artObj.user.username}
        }
        resComment = [
            {
                "comment": i.comment,
                "publish_date": str(i.publish_date),
                "user": {"id": i.user.id, "username": i.user.username},
                "parent": i.parent_id
            } for i in commentData
        ]

        artData['comment'] = resComment
        return HttpResponse(json.dumps(artData), content_type="application/json")

    def post(self, request, *args, **kwargs):
        article = form.ArticlesForm(request.POST)
        if not article.is_valid():
            return HttpResponse("发布失败!!!!!,{}".format(article.errors))

        articleData = article.cleaned_data
        user_id = request.session.get("user_id", 2)
        articleData['user_id'] = user_id
        articleRes = luntanmodel.Articles.objects.create(**articleData)

        topic = request.POST.get("topics", 0)
        if topic:
            topicObj = luntanmodel.Topics.objects.get(pk=topic)
            articleRes.topics.add(topicObj)

        return HttpResponse("发布成功！！！！！！")


# 评论
class Comment(views.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("ok!!!!!!")

    def post(self, request, *args, **kwargs):
        user_id = request.session.get("user_id", 2)
        data = json.loads(request.body)
        article = get_object_or_404(luntanmodel.Articles, pk=data.get("articles_id", 0))
        if data.get("parent_id", 0):
            parent_comment = get_object_or_404(luntanmodel.Comment, pk=data['parent_id'])

        data['user_id'] = user_id
        luntanmodel.Comment.objects.create(**data)
        return HttpResponse("评论成功！！！！！！！！！！")

