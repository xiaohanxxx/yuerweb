from django.db import models

# Create your models here.


class BaikeArea(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)


class BaikeArtical(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(BaikeArea, on_delete=models.CASCADE)