from django.db import models


# Create your models here.

# 交流圈
class Areas(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="交流圈名称")

    class Meta:
        verbose_name = "交流圈"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 分类话题
class Topics(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="话题名称")
    area = models.ForeignKey('Areas', related_name='areas_topics',
                             verbose_name='所属交流圈', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "分类话题"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 帖子
class Articles(models.Model):
    title = models.CharField(max_length=255, verbose_name="帖子标题")
    content = models.CharField(max_length=255, verbose_name="帖子内容")
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name="发布日期")
    update_date = models.DateTimeField(auto_now=True, verbose_name="更新日期")
    isdelete = models.IntegerField(default=0, verbose_name="是否被删除(逻辑删除)")
    # user = models.ForeignKey("users.User", related_name="articles_user",
    #                          verbose_name="用户", on_delete=models.CASCADE)
    topics = models.ManyToManyField("Topics", verbose_name='所属交流圈')

    class Meta:
        verbose_name = "帖子"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 评论
class Comment(models.Model):
    comment = models.TextField(max_length=1000, verbose_name="内容")
    articles = models.ForeignKey('Articles', related_name='articles_comment',
                                 on_delete=models.CASCADE, verbose_name="评论的帖子")
    # user = models.ForeignKey("users.User", related_name='comment_user',
    #                          on_delete=models.CASCADE, verbose_name="评论用户")
    publish_date = models.DateTimeField(auto_now=True, verbose_name="评论日期")
    parent = models.ForeignKey("self", related_name='parrent_comment',
                               blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "评论"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment


# 点赞
class ThumbUp(models.Model):
    articles = models.ForeignKey('Articles', related_name="thumup_articles",
                                 on_delete=models.CASCADE, verbose_name="点赞的文章")
    # user = models.ForeignKey('users.User', related_name="thumup_user",
    #                          on_delete=models.CASCADE, verbose_name="点赞用户")
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "点赞"  # 在admin站点显示名称
        verbose_name_plural = verbose_name


# class PostArtical(models.Model):
#     """帖子表"""
#     title = models.CharField(u'文章标题', max_length=255, unique=True)
#     category = models.ForeignKey("Category", verbose_name='板块名称', on_delete=models.CASCADE)
#     # 上传文件
#     # head_img = models.ImageField(upload_to="uploads")
#     content = models.TextField(verbose_name=u"正文")
#     # 文章作者
#     author = models.ForeignKey("users.User", verbose_name="作者", on_delete=models.CASCADE)
#     # 发布日期
#     publish_date = models.DateTimeField(auto_now=True, verbose_name="发布日期")
#
#     def __unicode__(self):
#         return "<%s,author:%s>" % (self.title, self.author)
#
#
# class Comment(models.Model):
#     """评论表"""
#     article = models.ForeignKey("PostArtical", on_delete=models.CASCADE, null=False)
#     # 评论用户
#     user = models.ForeignKey("users.User", on_delete=models.CASCADE)
#     # 评论内容
#     comment = models.TextField(max_length=1000)
#     # 评论时间
#     date = models.DateTimeField(auto_now=True)
#     # 父评论id
#     parent_comment = models.ForeignKey("self", related_name='p_comment', blank=True, null=True,
#                                        on_delete=models.CASCADE)
#
#     def __unicode__(self):
#         return "<user:%s>" % (self.user)
#
#
# class ThumbUp(models.Model):
#     """点赞"""
#     # 给那个文章点的
#     article = models.ForeignKey('PostArtical', on_delete=models.CASCADE)
#     # 用户名
#     user = models.ForeignKey('users.User', on_delete=models.CASCADE)
#     # 时间
#     date = models.DateTimeField(auto_now=True)
#
#
# class Category(models.Model):
#     """板块表"""
#     name = models.CharField(max_length=255, unique=True, verbose_name="板块名称")
#
#     def __unicode__(self):
#         return self.name
