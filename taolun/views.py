import json

from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.shortcuts import render, HttpResponse, get_object_or_404
from django import views
from . import models, form


# Create your views here.
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
                    res.append({"id": k.id, "name": k.name})

        else:
            groupObj = get_object_or_404(models.Groups, pk=groupId)
            topics = groupObj.group_topics.all()
            for i in topics:
                res.append({"id": i.id, "name": i.name})

        return HttpResponse(json.dumps(res))


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
            postList = topicObj.topics_set.all().order_by('update_date')
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
             "user": {"id": i.user.id, "username": i.user.username, "head": str(i.user.info.user_avatar)}
             } for i in curuent_page
        ]
        return HttpResponse(json.dumps(res))


# 获取帖子
class Posting(views.View):
    def get(self, request, *args, **kwargs):
        postingId = request.GET.get('pid')
        postingData = get_object_or_404(models.Posting, pk=postingId)
        # 获取帖子发布人信息
        postingData.userData = postingData.user
        # 获取帖子评论信息
        commentData = postingData.articles_comment.all()
        for i in commentData:
            commentData.userData = i.user
        return HttpResponse("帖子：{}，评论：{}".format(postingData, commentData))

    def post(self, request, *args, **kwargs):
        posting = form.PostingForm(request.POST)
        if not posting.is_valid():
            return HttpResponse("发布失败!!!!!,{}".format(posting.errors))

        postingData = posting.cleaned_data
        user_id = request.session.get("user_id", 2)
        postingData['user_id'] = user_id
        postingRes = models.Posting.objects.create(**postingData)

        topic = request.POST.get("topics", 0)
        if topic:
            topicObj = models.Topics.objects.get(pk=topic)
            postingRes.topics.add(topicObj)

        return HttpResponse("发布成功！！！！！！")


# 评论
class Comment(views.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("ok!!!!!!")

    def post(self, request, *args, **kwargs):
        user_id = request.session.get("user_id", 2)
        data = json.loads(request.body)
        article = get_object_or_404(models.Posting, pk=data.get("articles_id", 0))
        if data.get("parent_id", 0):
            parent_comment = get_object_or_404(models.Comment, pk=data['parent_id'])

        data['user_id'] = user_id
        models.Comment.objects.create(**data)
        return HttpResponse("评论成功！！！！！！！！！！")
