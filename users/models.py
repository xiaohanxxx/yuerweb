from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.


class Userinfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    user_avatar = models.ImageField('用户头像', upload_to='user_avatar', default='/user_avatar/touxiang.jpg')
    integral = models.IntegerField('积分', default=0)

    Virtual_choice = (
        (0, '青铜'),
        (1, '白银'),
        (2, '黄金'),
    )
    level = models.IntegerField('等级', choices=Virtual_choice, default=0)
    phone = models.CharField('手机号', max_length=20)


    def image_img(self):
        if self.user_avatar:
            # TODO 上线后需要修改为上线地址
            # print('http://127.0.0.1:8000/media/%s'%self.cover)
            return mark_safe('<img src="http://127.0.0.1:8000/media/%s" style="width: 100px"/>' % self.user_avatar)
        else:
            return u'图片'


    def __str__(self):
        return self.user.username
    #     return User.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


# 关注模型
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE, verbose_name="关注者")  # 关注者
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE, verbose_name="被关注者")  # 被关注者
    date = models.DateTimeField(auto_now_add=True, verbose_name="关注时间")  # 关注时间

    class Meta:
        ordering = ('-date',)
        verbose_name = '用户关注'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.follower} 关注 {self.followed}'

    @staticmethod
    def unfollow(from_user, to_user):
        f = Follow.objects.filter(follower=from_user, followed=to_user).all()
        if f:
            f.delete()  # 取关

    # 得到当前用户关注的人
    @staticmethod
    def user_followed(from_user):
        followeders = Follow.objects.filter(follower=from_user).all()
        user_followed = []
        for followeder in followeders:
            user_followed.append({'username': followeder.followed.username, 'userid': followeder.followed.id,'user_avatar':followeder.followed.info.user_avatar.url})
        return user_followed  # list

    # 得到当前用户的粉丝
    @staticmethod
    def user_follower(from_user):
        followeders = Follow.objects.filter(followed=from_user).all()
        user_followed = []
        for followeder in followeders:
            Quser = User.objects.get(id=followeder.follower_id)
            # 判断是否互相关注
            t = Follow.objects.filter(follower=from_user, followed=Quser).all()
            if t:
                user_followed.append(
                    {'username': followeder.follower.username, 'userid': followeder.follower.id,'user_avatar':followeder.follower.info.user_avatar.url,
                     'mutualfollower': 0})  # 0表示互相关注
            else:
                user_followed.append(
                    {'username': followeder.follower.username, 'userid': followeder.follower.id,'user_avatar':followeder.follower.info.user_avatar.url,
                     'mutualfollower': 1})  # 1表示未关注粉丝

        return user_followed  # 得到from_user关注的人，返回列表
















