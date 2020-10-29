from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class PostArtical(models.Model):
    """帖子表"""
    title = models.CharField(u'文章标题', max_length=255, unique=True)
    category = models.ForeignKey("Category", verbose_name='板块名称', on_delete=models.CASCADE)
    # 上传文件
    # head_img = models.ImageField(upload_to="uploads")
    content = models.TextField(verbose_name=u"正文")
    # 文章作者
    author = models.ForeignKey("users.User", verbose_name="作者", on_delete=models.CASCADE)
    # 发布日期
    publish_date = models.DateTimeField(auto_now=True, verbose_name="发布日期")

    def __unicode__(self):
        return "<%s,author:%s>" % (self.title, self.author)


class Comment(models.Model):
    """评论表"""
    article = models.ForeignKey("PostArtical", on_delete=models.CASCADE, null=False)
    # 评论用户
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    # 评论内容
    comment = models.TextField(max_length=1000)
    # 评论时间
    date = models.DateTimeField(auto_now=True)
    # 父评论id
    parent_comment = models.ForeignKey("self", related_name='p_comment', blank=True, null=True,
                                       on_delete=models.CASCADE)

    def __unicode__(self):
        return "<user:%s>" % (self.user)


class ThumbUp(models.Model):
    """点赞"""
    # 给那个文章点的
    article = models.ForeignKey('PostArtical', on_delete=models.CASCADE)
    # 用户名
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    # 时间
    date = models.DateTimeField(auto_now=True)


class Category(models.Model):
    """板块表"""
    name = models.CharField(max_length=255, unique=True, verbose_name="板块名称")

    def __unicode__(self):
        return self.name
