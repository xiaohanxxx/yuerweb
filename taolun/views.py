import json

from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, get_object_or_404
from django import views
from . import models, form


# Create your views here.
# 获取讨论组
class Groups(views.View):
    def get(self, request, *args, **kwargs):
        data = models.Groups.objects.all()
        return HttpResponse("交流圈有：{}".format(data))


# 获取分类话题
class Topics(views.View):
    def get(self, request, *args, **kwargs):
        groupId = request.GET.get('gid')
        groupObj = get_object_or_404(models.Groups, pk=groupId)
        topics = groupObj.group_topics.all()
        return HttpResponse("{}包含的分类话题有：{}".format(groupObj.name, topics))


# 获取分类话题列表
class PostingList(views.View):
    def get(self, request, *args, **kwargs):
        topicsId = request.GET.get('tid')
        topicsData = models.Topics.objects.get(pk=topicsId)
        postingList = topicsData.posting_set.all().order_by("update_date")
        curuent_page_num = request.GET.get("page", 1)  # 获取当前页数,默认为1
        paginator = Paginator(postingList, 10)
        pag_num = paginator.num_pages  # 获取整个表的总页数
        curuent_page = paginator.page(curuent_page_num)  # 获取当前页的数据
        for i in curuent_page:
            print(i.title)
            print(i.content)
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
                curuent_page_num, pag_num, pag_range, curuent_page
            )
        )


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