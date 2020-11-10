from django.db import models
from django.contrib.auth.models import User
import markdown
from django.utils.html import strip_tags
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Bk_menu(models.Model):
    menu_name = models.CharField('栏目名称',max_length=50)
    is_active = models.BooleanField('显示',default=True)
    idx = models.IntegerField('排序')

    def __str__(self):
        return self.menu_name

    class Meta:
        verbose_name = '百科主栏目'
        verbose_name_plural = verbose_name




# 百科分类
class Child_menu(models.Model):
    child_name = models.CharField('子栏目名称',max_length=50)
    relation = models.ForeignKey(Bk_menu, on_delete=models.CASCADE, blank=True, null=True, verbose_name='上级栏目')
    is_active = models.BooleanField('显示', default=True)
    idx = models.IntegerField('排序')


    def __str__(self):
        return self.child_name

    class Meta:
        verbose_name = '二级分类'
        verbose_name_plural = verbose_name


class Menu(models.Model):
    child_name = models.CharField('栏目名称',max_length=50)
    relation = models.ForeignKey(Child_menu, on_delete=models.CASCADE, blank=True, null=True, verbose_name='上级栏目')
    is_active = models.BooleanField('显示', default=True)
    idx = models.IntegerField('排序')


    def __str__(self):
        return self.child_name

    class Meta:
        verbose_name = '三级分类'
        verbose_name_plural = verbose_name



class Artical(models.Model):
    title = models.CharField('标题',max_length=100)
    category = models.ForeignKey(Menu,on_delete=models.CASCADE, blank=True, null=True, verbose_name='文章栏目')
    author = models.CharField('作者',max_length=30,default='育儿网')
    thumb = models.ImageField(upload_to='thumbnail')
    content = RichTextUploadingField('内容')
    excerpt = models.CharField('摘要',max_length=100,blank=True)
    click_count = models.IntegerField('点击次数',default=0)
    add_time = models.DateTimeField('发布时间',auto_now_add=True)


    def save(self, *args, **kwargs):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        self.excerpt = strip_tags(md.convert(self.content))[:87]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.title
