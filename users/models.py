from django.db import models


# Create your models here.


class User(models.Model):
    user_name = models.CharField('用户名', max_length=128, unique=True)
    user_pwd = models.CharField('密码', max_length=255)
    user_email = models.EmailField('邮箱', unique=True)
    user_phone = models.CharField('手机号', max_length=50, unique=True)
    grade_choice = (
        (0, '普通会员'),
        (1, 'V1会员'),
        (2, 'V2会员'),
        (3, 'V3会员'),
        (4, 'V4会员'),
        (5, 'S1会员'),
        (6, 'S2会员'),
        (7, 'S3会员'),
        (8, 'S4会员'),
    )

    user_grade = models.IntegerField('用户等级', choices=grade_choice, default=0)
    user_yuliang = models.CharField('余量', max_length=30, default='5')

    user_state = models.BooleanField('用户状态', default=True)
    add_time = models.DateTimeField('注册时间', auto_now_add=True)

    head_photo = models.ImageField('头像',upload_to='user/image')


    def __str__(self):
        return self.user_name


    def ge_avatar_url(self):
        '''返回头像的url'''
        return '域名/media' + str(self.head_photo)

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name


# 前端展示
# <img width="100" height="100"  data-url="{{ MEDIA_URL }}{{ user.image }}"/>