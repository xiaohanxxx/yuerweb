from django.db import models
from django.contrib.auth.models import User
import markdown
from django.utils.html import strip_tags
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe

# Create your models here.
# 百科主栏目模型
class Bk_menu(models.Model):
    menu_name = models.CharField('栏目名称',max_length=50)
    is_active = models.BooleanField('显示',default=True)
    baike_images = models.ImageField('栏目图片', upload_to='baike', default='/baike/default.png')

    def __str__(self):
        return self.menu_name

    class Meta:
        verbose_name = '百科主栏目'
        verbose_name_plural = verbose_name

# 子栏目模型
class Child_menu(models.Model):
    menu_name = models.CharField('子栏目名称',max_length=50)
    relation = models.ForeignKey(Bk_menu, on_delete=models.CASCADE, blank=True, null=True, verbose_name='上级栏目')
    is_active = models.BooleanField('显示', default=True)

    def __str__(self):
        return self.menu_name

    class Meta:
        verbose_name = '二级分类'
        verbose_name_plural = verbose_name

# 文章模型
class Artical(models.Model):
    title = models.CharField('标题',max_length=100)
    category = models.ForeignKey(Child_menu,on_delete=models.CASCADE, blank=True, null=True, verbose_name='文章栏目')
    recommend = models.BooleanField('推荐',default=False)
    author = models.CharField('作者',max_length=30,default='育儿网')
    thumb = models.ImageField('缩略图',upload_to='thumbnail')
    content = RichTextUploadingField('内容')
    excerpt = models.CharField('摘要',max_length=100,blank=True)
    click_count = models.IntegerField('点击次数',default=0)
    add_time = models.DateTimeField('发布时间',auto_now_add=True)


    def image_img(self):
        if self.thumb:
            # TODO 上线后需要修改为上线地址
            # print('http://127.0.0.1:8000/media/%s'%self.cover)
            return mark_safe('<img src="http://127.0.0.1:8000/media/%s" style="width: 100px"/>' % self.thumb)
        else:
            return u'图片'


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