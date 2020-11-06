import json

from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, get_object_or_404
from django import views
from . import models as luntanmodel
from . import form


# Create your views here.


# 获取交流圈
class Areas(views.View):
    def get(self, request, *args, **kwargs):
        data = luntanmodel.Areas.objects.all()
        return render(request, 'yuerlt.html', {"data": data})


# 获取分类话题
class Topics(views.View):
    def get(self, request, *args, **kwargs):
        areaId = request.GET.get('aid')
        areaObj = get_object_or_404(luntanmodel.Areas, pk=areaId)
        topics = areaObj.areas_topics.all()
        return HttpResponse("{}包含的分类话题有：{}".format(areaObj.name, topics))


# 获取分类帖子列表
class ArticlesList(views.View):
    def get(self, request, *args, **kwargs):
        topicsId = request.GET.get('tid')
        topicsData = luntanmodel.Topics.objects.get(pk=topicsId)
        articleList = topicsData.articles_set.all().order_by("id")
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

        return HttpResponse(
            "这是第{}页的数据，一共有{}页数据，页码列表是{}，本页数据内容是/r/n{}".format(
                curuent_page_num, pag_num, pag_range, curuent_page
            )
        )


# 获取帖子
class Article(views.View):
    def get(self, request, *args, **kwargs):
        articleId = request.GET.get('aid')
        articleData = get_object_or_404(luntanmodel.Articles, pk=articleId)
        # 获取帖子发布人信息
        articleData.userData = articleData.user
        # 获取帖子评论信息
        commentData = articleData.articles_comment.all()
        for i in commentData:
            commentData.userData = i.user
        return HttpResponse("帖子：{}，评论：{}".format(articleData, commentData))

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


# if __name__ == '__main__':
#     models.Areas.objects.create(name="备孕交流圈")
#     models.Areas.objects.create(name="妈妈交流圈")
#     models.Areas.objects.create(name="试管婴儿交流圈")
#     models.Areas.objects.create(name="难孕交流圈")
#
#     # 插分类
#     for n in range(1, 5):
#         data = models.Areas.objects.get(pk=n)
#         for i in range(1, 4):
#             k = str(data.name) + str(i)
#             models.Topics.objects.create(name=k, area=data)
#
#     # 插帖子
#     for i in range(1, 14):
#         articles = luntanmodel.Articles.objects.create(title="xxxx", content="xxxx", user_id=2)
#         topics = luntanmodel.Topics.objects.get(pk=i)
#         articles.topics.add(topics)
