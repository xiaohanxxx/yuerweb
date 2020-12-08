from django.db import models
from django.utils.safestring import mark_safe

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


# 首页banner
class Banner(models.Model):
    title = models.CharField('标题', max_length=50)
    cover = models.ImageField('轮播图', upload_to='banner/index')
    banner_link = models.URLField('对应链接',default='https://www.zhimeiai.cn')
    idx = models.IntegerField('索引')
    is_active = models.BooleanField('是否是active', default=False)
    add_time = models.DateTimeField('添加时间',auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = '首页轮播图'

    def image_img(self):
        if self.cover:
            # TODO 上线后需要修改为上线地址
            # print('http://127.0.0.1:8000/media/%s'%self.cover)
            return mark_safe('<img src="http://127.0.0.1:8000/media/%s" style="width: 100px"/>' % self.cover)
        else:
            return u'图片'

    image_img.short_description = '缩略图显示'
    image_img.allow_tags = True


# 百科Banner
class BaikeBanner(models.Model):
    title = models.CharField('标题', max_length=50)
    cover = models.ImageField('轮播图', upload_to='banner/index')
    baikebanner_link = models.URLField('对应链接',default='https://www.zhimeiai.cn')
    idx = models.IntegerField('索引')
    is_active = models.BooleanField('是否是active', default=False)

    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '百科轮播图'
        verbose_name_plural = '百科轮播图'

    def image_img(self):
        if self.cover:
            # TODO 上线后需要修改为上线地址
            # print('http://127.0.0.1:8000/media/%s'%self.cover)
            return mark_safe('<img src="http://127.0.0.1:8000/media/%s" style="width: 100px"/>' % self.cover)
        else:
            return u'图片'

    image_img.short_description = '缩略图显示'
    image_img.allow_tags = True


# 论坛轮播图
class YuerBanner(models.Model):
    title = models.CharField('标题', max_length=50)
    cover = models.ImageField('轮播图', upload_to='banner/index')
    yuerbanner_link = models.URLField('对应链接',default='http://www.zhimeiai.cn')
    idx = models.IntegerField('索引')
    is_active = models.BooleanField('是否是active', default=False)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '论坛轮播图'
        verbose_name_plural = '论坛轮播图'

    def image_img(self):
        if self.cover:
            # TODO 上线后需要修改为上线地址
            # print('http://127.0.0.1:8000/media/%s'%self.cover)
            return mark_safe('<img src="http://127.0.0.1:8000/media/%s" style="width: 100px"/>' % self.cover)
        else:
            return u'图片'

    image_img.short_description = '缩略图显示'
    image_img.allow_tags = True