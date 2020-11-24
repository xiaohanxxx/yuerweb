from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 讨论组
class Groups(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="讨论组名称")

    class Meta:
        verbose_name = "讨论组"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 分类话题
class Topics(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="话题名称")
    thumb = models.ImageField(verbose_name='缩略图', default="/media/thumbnail/824.png", upload_to='thumbnail')
    area = models.ForeignKey('Groups', related_name='group_topics',
                             verbose_name='所属讨论组', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "分类话题"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 帖子
class Posting(models.Model):
    title = models.CharField(max_length=255, verbose_name="帖子标题")
    content = models.CharField(max_length=255, verbose_name="帖子内容")
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name="发布日期")
    update_date = models.DateTimeField(auto_now=True, verbose_name="更新日期")
    read = models.IntegerField(default=1, verbose_name="浏览量")
    isdelete = models.IntegerField(default=0, verbose_name="是否被删除(逻辑删除)")
    user = models.ForeignKey(User, related_name="posting_user",
                             verbose_name="用户", on_delete=models.CASCADE)
    topics = models.ManyToManyField("Topics", verbose_name='所属话题')

    class Meta:
        verbose_name = "帖子"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 评论
class Comment(models.Model):
    comment = models.TextField(max_length=999, verbose_name="评论内容")
    articles = models.ForeignKey('Posting', related_name='posting_comment',
                                 on_delete=models.CASCADE, verbose_name="评论的帖子")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论用户")
    publish_date = models.DateTimeField(auto_now=True, verbose_name="评论日期")
    parent = models.ForeignKey("self", related_name='parent_comment',
                               blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "评论"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment

