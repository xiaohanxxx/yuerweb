from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Userinfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='info')
    phone = models.CharField('手机号',max_length=20)

