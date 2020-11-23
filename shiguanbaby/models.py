from django.db import models


# Create your models here.

class Areas(models.Model):
    name = models.CharField(max_length=255, verbose_name="地区")

    class Meta:
        verbose_name = "地区"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 分类标签
class Topics(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="标签名称")

    class Meta:
        verbose_name = "分类标签"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章类型
class ArticleType(models.Model):
    name = models.CharField(max_length=255, verbose_name="文章类型")

    class Meta:
        verbose_name = "文章类型"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章
class Articles(models.Model):
    title = models.CharField(max_length=255, verbose_name="文章标题")
    content = models.CharField(max_length=255, verbose_name="文章内容")
    area = models.ForeignKey("Areas", on_delete=models.CASCADE, verbose_name="所属地区")
    thumb = models.ImageField(verbose_name='缩略图', default="/media/thumbnail/824.png", upload_to='thumbnail')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name="发布日期")
    update_date = models.DateTimeField(auto_now=True, verbose_name="更新日期")
    isdelete = models.IntegerField(default=0, verbose_name="是否被删除(逻辑删除)")
    user = models.CharField(max_length=255, verbose_name="作者")
    topics = models.ManyToManyField("Topics", verbose_name='标签')
    type = models.ManyToManyField("ArticleType", verbose_name="文章类型")

    class Meta:
        verbose_name = "文章"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
