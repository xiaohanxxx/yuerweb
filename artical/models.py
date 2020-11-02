from django.db import models

# Create your models here.
from django.utils import timezone


# class Area(models.Model):
#     name = models.CharField(max_length=255, verbose_name=u'地区', unique=True)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, verbose_name='自关联')
#
#     class Meta:
#         verbose_name = "地区"  # 在admin站点显示名称
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
#
#
# class ArticalType(models.Model):
#     name = models.CharField(max_length=255, verbose_name=u'文章类别', unique=True)
#
#     class Meta:
#         verbose_name = "文章分类"  # 在admin站点显示名称
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
#
#
# class Artical(models.Model):
#     title = models.CharField(max_length=100, verbose_name=u'标题')
#     content = models.TextField(verbose_name=u'正文')
#     create_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
#     area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name=u'地区')
#     artical_type = models.ManyToManyField(ArticalType, verbose_name=u'文章标签')
#
#     class Meta:
#         verbose_name = "文章"  # 在admin站点显示名称
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.title
