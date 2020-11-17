from django.db import models

# Create your models here.

class FriendLink(models.Model):
    link_name = models.CharField('网站名称',max_length=50)
    link = models.CharField('网址',max_length=100)
    idx = models.IntegerField('排列位置',default=0)

    def __str__(self):
        return self.link_name

    class Meta:
        verbose_name = '友链管理'
        verbose_name_plural = verbose_name