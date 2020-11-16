from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Userinfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='info')
    user_avatar = models.ImageField('用户头像',upload_to='user_avatar',default='/user_avatar/touxiang.jpg')
    phone = models.CharField('手机号',max_length=20)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
