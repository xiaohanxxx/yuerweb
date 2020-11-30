import json
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.shortcuts import render, HttpResponse, get_object_or_404
from django import views
from django.utils.decorators import method_decorator

from yuerweb import settings
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
                "child": [{"id": k.id, "name": k.name, "thumb": k.thumb.url, "child": []} for k in i.areas_topics.all()]} for i in
               areasObjList]
        return HttpResponse(json.dumps({"data": res}), content_type="application/json")


# 获取分类话题
class Topics(views.View):
    def get(self, request, *args, **kwargs):
        areaId = request.GET.get('aid')
        areaObj = get_object_or_404(luntanmodel.Areas, pk=areaId)
        topics = areaObj.areas_topics.all()
        areaData = [{"id": i.id, "name": i.name, "thumb": i.thumb.url} for i in topics]
        return HttpResponse(json.dumps({"data": areaData}), content_type="application/json")


# 获取分类帖子列表
class ArticlesList(views.View):
    def get(self, request, *args, **kwargs):
        topicsId = request.GET.get('tid')
        num = request.GET.get('num', 10)
        type = request.GET.get('type', 1)
        topicsData = luntanmodel.Topics.objects.get(pk=int(topicsId))
        # 最新
        if int(type) == 1:
            articleList = topicsData.articles_set.filter(isdelete=0).order_by("-publish_date")
        # 热门
        elif int(type) == 2:
            thumbList = luntanmodel.ThumbUp.objects.filter(articles__topics=topicsId, articles__isdelete=0).values(
                'articles_id').annotate(count=Count('articles_id'))
            aidList = [i["articles_id"] for i in thumbList]
            articleList = luntanmodel.Articles.objects.filter(pk__in=aidList)
        # 推荐
        else:
            articleList = topicsData.articles_set.filter(isdelete=0).order_by("read")
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
            "maxnum": len(articleList),
            "curuent_page": [
                {
                    "id": i.id,
                    "title": i.title,
                    "content": i.content,
                    "publish_date": str(i.publish_date),
                    "user": {"id": i.user.id, "username": i.user.username, "head": str(i.user.info.user_avatar)},
                    "commentnum": i.articles_comment.all().count(),
                    "thumbup": i.thumup_articles.all().count()
                } for i in curuent_page
            ]
        }
        if request.GET.get('all'):
            return render(request, 'beiyunjiaoliu.html', {"data": res})
        return HttpResponse(json.dumps({"data": res}), content_type="application/json")


# 获取帖子
class Article(views.View):
    def get(self, request, *args, **kwargs):
        articleId = request.GET.get('aid')
        artObj = get_object_or_404(luntanmodel.Articles, pk=articleId)
        # 阅读计数
        luntanmodel.Articles.objects.update(read=F("read") + 1)
        # 获取帖子发布人信息
        artData = {
            "id": artObj.id,
            "title": artObj.title,
            "content": artObj.content,
            "publish_date": artObj.publish_date,
            "user": {"id": artObj.user.id, "username": artObj.user.username, "head": str(artObj.user.info.user_avatar)},
            "thumbup": artObj.thumup_articles.all().count()
        }

        return render(request, 'topicArc.html', {"data": artData})

    def post(self, request, *args, **kwargs):
        articleData = {
            "user_id": request.user.id,
            "title": request.POST.get("title"),
            "content": request.POST.get("content")
        }
        articleRes = luntanmodel.Articles.objects.create(**articleData)

        topic = request.POST.getlist("topic", [])

        if topic:
            topicObj = luntanmodel.Topics.objects.get(pk__in=topic)
            articleRes.topics.add(topicObj)

        return HttpResponse(json.dumps({"data": articleRes.id}))


# 评论
class Comment(views.View):
    def get(self, request, *args, **kwargs):
        articleId = request.GET.get('articles_id')
        artObj = get_object_or_404(luntanmodel.Articles, pk=articleId)
        commentData = artObj.articles_comment.all()
        resComment = [
            {
                "id": i.id,
                "comment": i.comment,
                "publish_date": str(i.publish_date),
                "user": {"id": i.user.id, "username": i.user.username, "head": str(artObj.user.info.user_avatar)},
                "parent": i.parent_id
            } for i in commentData
        ]
        return HttpResponse(json.dumps({"data": resComment}))

    def post(self, request, *args, **kwargs):
        data = {k: v for k, v in request.POST.items()}
        article = get_object_or_404(luntanmodel.Articles, pk=data.get("articles_id", 0))
        if data.get("parent_id", 0):
            parent_comment = get_object_or_404(luntanmodel.Comment, pk=data['parent_id'])

        data['user_id'] = request.user.id
        luntanmodel.Comment.objects.create(**data)
        return HttpResponse("评论成功！！！！！！！！！！")


# 获取热门文章
class HotAritcles(views.View):
    def get(self, request, *args, **kwargs):
        thumbList = luntanmodel.ThumbUp.objects.values('articles_id').annotate(count=Count('articles_id'))[:30]
        aidList = [i["articles_id"] for i in thumbList]
        atList = luntanmodel.Articles.objects.filter(pk__in=aidList)
        atDict = {}
        for i in atList:
            atDict[i.id] = {
                'id': i.id,
                "title": i.title,
                "content": i.content,
                "update_date": str(i.update_date),
                "user": {
                    "id": i.user.id,
                    "username": i.user.username,
                    "head": str(i.user.info.user_avatar),
                }
            }

        resList = []
        for i in thumbList:
            data = {
                "article": atDict[i["articles_id"]],
                "thumb": i["count"]
            }
            resList.append(data)

        return HttpResponse(json.dumps({"data": resList}))


# 好运妈妈榜
class GoodMother(views.View):
    def get(self, request, *args, **kwargs):
        aid = request.GET.get("aid")
        num = request.GET.get("num", 10)
        curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
        artclesList = luntanmodel.Articles.objects.filter(topics__area=aid).order_by("update_date")
        paginator = Paginator(artclesList, num)
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
                    "topicname": list(i.topics.all().values()),
                    "title": i.title,
                    "user": {"id": i.user.id, "username": i.user.username, "head": str(i.user.info.user_avatar)},
                    "commentnum": i.articles_comment.all().count()
                } for i in curuent_page
            ]
        }

        return HttpResponse(json.dumps({"data": res}), content_type="application/json")


class ThumbUp(views.View):
    def get(self, request, *args, **kwargs):
        aid = request.GET.get("aid")
        artObj = get_object_or_404(luntanmodel.Articles, pk=aid)
        uid = request.user.id
        userObj = get_object_or_404(User, pk=uid)
        chk = luntanmodel.ThumbUp.objects.filter(articles_id=aid, user_id=uid)
        if chk:
            return HttpResponse("已点赞, 无法重复点赞")
        thumb = luntanmodel.ThumbUp()
        thumb.articles = artObj
        thumb.user = userObj
        thumb.save()
        return HttpResponse("点赞成功")


class ImageUp(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'imageuptest.html')

    def post(self, request):
        avatar = request.FILES.get('upload')
        dir = 'media/luntan/' + avatar.name
        with open(dir, 'wb') as f:
            for line in avatar:
                f.write(line)

        return HttpResponse(json.dumps({"file": avatar.name, "uploaded": 1, "url": "/" + dir}))


class PostAritcle(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'post.html')


# 获取我的帖子
@method_decorator(login_required, name='dispatch')
class GetMyArticles(views.View):
    def get(self, request, *args, **kwargs):
        uid = request.user.id
        articleObjList = luntanmodel.Articles.objects.filter(user_id=uid)
        num = request.GET.get("num", 10)
        curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
        paginator = Paginator(articleObjList, num)
        curuent_page = paginator.page(curuent_page_num)     # 获取当前页的数据
        res = []
        for i in curuent_page:
            res.append({
                "id": i.id,
                "title": i.title,
                "content": i.content,
                "publish_date": str(i.publish_date),
                "thumbup": i.thumup_articles.all().count(),
                "commentnum": i.articles_comment.all().count(),
            })
        return HttpResponse(json.dumps({"data": res, "maxnum": len(articleObjList)}))