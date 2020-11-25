import json

from django.core.paginator import Paginator
from django.db.models import F, Count
from django.forms import model_to_dict
from django.shortcuts import render, HttpResponse, get_object_or_404
from django import views
from . import models, form


# Create your views here.

class Index(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'huzhuwenda.html')


class ToGroups(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'huzhuluntanlist.html')


# 帖子界面
class ToPosting(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'huzhulundainfo.html')


# 发帖界面
class ToPost(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hzwdpost.html')


# 栏目小组
class GroupList(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hzwdadd.html')


# 获取讨论组
class Groups(views.View):
    def get(self, request, *args, **kwargs):
        data = models.Groups.objects.all()
        res = [{"id": i.id, "name": i.name} for i in data]
        return HttpResponse(json.dumps(res))


# 获取分类话题
class Topics(views.View):
    def get(self, request, *args, **kwargs):
        groupId = request.GET.get('gid')
        res = []
        # 获取所有分类话题
        if groupId == '999':
            gList = models.Groups.objects.all()
            for i in gList:
                tList = i.group_topics.all()
                for k in tList:
                    count = models.Topics.objects.filter(id=k.id).values("id", 'name').annotate(
                        count=Count('posting__posting_comment__id'))
                    res.append({"id": k.id, "name": k.name, "thumb": k.thumb.url, "topicontent": k.topicontent, "topicnum": count[0]['count']})

        else:
            groupObj = get_object_or_404(models.Groups, pk=groupId)
            tList = groupObj.group_topics.all()
            for i in tList:
                count = models.Topics.objects.filter(id=i.id).values("id", 'name').annotate(
                    count=Count('posting__posting_comment__id'))
                res.append({"id": i.id, "name": i.name, "thumb": i.thumb.url, "topicontent": i.topicontent, "topicnum": count[0]['count']})

        num = request.GET.get('num', 10)
        curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
        paginator = Paginator(res, num)

        curuent_page = paginator.page(curuent_page_num)  # 获取当前页的数据
        return HttpResponse(json.dumps({"data": curuent_page.object_list, "maxnum": len(res)}))


# 获取分类话题列表
class PostingList(views.View):
    def get(self, request, *args, **kwargs):
        topicsId = request.GET.get('tid', 0)
        # 获取全部
        if not topicsId:
            # 最新
            postList = models.Posting.objects.all().order_by('update_date')
            chk = request.GET.get('order', 0)
            # 热门
            if chk == '1':
                postList = models.Posting.objects.all().order_by('read')
            # 等待回复
            elif chk == '2':
                postList = models.Posting.objects.filter(read__lte=10).order_by('read', 'update_date')

            num = request.GET.get('num', 10)
            curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
            paginator = Paginator(postList, num)
            curuent_page = paginator.page(curuent_page_num)  # 获取当前页的数据

        # 获取指定分类话题列表
        else:
            topicObj = get_object_or_404(models.Topics, id=topicsId)
            # 最新
            postList = topicObj.posting_set.all().order_by('update_date')
            chk = request.GET.get('order', 0)
            # 热门
            if chk == "1":
                postList = topicObj.topics_set.all().order_by('read')

            num = request.GET.get('num', 10)
            curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
            paginator = Paginator(postList, num)
            curuent_page = paginator.page(curuent_page_num)  # 获取当前页的数据

        res = [
            {"id": i.id,
             "title": i.title,
             "content": i.content,
             "publish_date": str(i.publish_date),
             "update_date": str(i.update_date),
             "read": i.read,
             "commentnum": i.posting_comment.all().count(),
             "user": {"id": i.user.id, "username": i.user.username, "head": str(i.user.info.user_avatar)}
             } for i in curuent_page
        ]
        return HttpResponse(json.dumps({"data": res, "maxnum": len(postList)}))


# 获取帖子
class Posting(views.View):
    def get(self, request, *args, **kwargs):
        postingId = request.GET.get('pid')
        postingObj = get_object_or_404(models.Posting, pk=postingId)
        # 阅读计数
        models.Posting.objects.update(read=F("read") + 1)
        # 获取帖子发布人信息
        artData = {
            "id": postingObj.id,
            "title": postingObj.title,
            "content": postingObj.content,
            "read": postingObj.read,
            "publish_date": str(postingObj.publish_date),
            "user": {"id": postingObj.user.id, "username": postingObj.user.username,
                     "head": str(postingObj.user.info.user_avatar)},
        }
        return HttpResponse(json.dumps({"data": artData}))

    def post(self, request, *args, **kwargs):
        articleData = {
            "user_id": request.user.id,
            "title": request.POST.get("title"),
            "content": request.POST.get("content")
        }
        postingRes = models.Posting.objects.create(**articleData)

        topic = request.POST.getlist("topics", [])

        if topic:
            topicObj = models.Topics.objects.get(pk__in=topic)
            postingRes.topics.add(topicObj)

        return HttpResponse(json.dumps({"data": postingRes.id}))


# 评论
class Comment(views.View):
    def get(self, request, *args, **kwargs):
        postingId = request.GET.get('pid')
        postingObj = get_object_or_404(models.Posting, pk=postingId)
        commentData = postingObj.posting_comment.all()
        resComment = [
            {
                "id": i.id,
                "comment": i.comment,
                "publish_date": str(i.publish_date),
                "user": {"id": i.user.id, "username": i.user.username, "head": str(postingObj.user.info.user_avatar)},
                "parent": i.parent_id
            } for i in commentData
        ]
        return HttpResponse(json.dumps({"data": resComment}))

    def post(self, request, *args, **kwargs):
        data = {k: v for k, v in request.POST.items()}
        postingObj = get_object_or_404(models.Posting, pk=data.get("pid", 0))
        if data.get("parent_id", 0):
            parent_comment = get_object_or_404(models.Comment, pk=data['parent_id'])

        data['user_id'] = request.user.id
        models.Comment.objects.create(**data)
        return HttpResponse("评论成功！！！！！！！！！！")


# 热门标签
class HotTopics(views.View):
    def get(self, request, *args, **kwargs):
        num = request.GET.get("num", 10)
        countList = models.Topics.objects.values('id', 'name').annotate(count=Count('posting__posting_comment__id')).order_by('-count')[:int(num)]
        return HttpResponse(json.dumps({"data": list(countList)}))


# 热门话题
class HotArticles(views.View):
    def get(self, request, *args, **kwargs):
        num = request.GET.get("num", 10)
        countList = models.Posting.objects.values('id', 'title').annotate(count=Count('posting_comment__id')).order_by('-count')[:int(num)]
        return HttpResponse(json.dumps({"data": list(countList)}))