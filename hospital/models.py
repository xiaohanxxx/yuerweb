from django.db import models


# Create your models here.

class Area(models.Model):
    name = models.CharField(max_length=255, verbose_name="地区")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, verbose_name='自关联')

    class Meta:
        verbose_name = "地区"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class HospitalLv(models.Model):
    name = models.CharField(max_length=255, verbose_name="等级")

    class Meta:
        verbose_name = "等级"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class HospitalType(models.Model):
    name = models.CharField(max_length=255, verbose_name="技术")

    class Meta:
        verbose_name = "技术"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Power(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")

    class Meta:
        verbose_name = "重点类型"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Hospital(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    content = models.TextField(verbose_name="正文")
    address = models.TextField(verbose_name="地址")
    phone = models.CharField(max_length=100, verbose_name="电话")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    worldarea = models.ForeignKey("Area", related_name="worldarea", on_delete=models.CASCADE, verbose_name="世界范围")
    privincearea = models.ForeignKey("Area", related_name="privincearea", on_delete=models.CASCADE, verbose_name="省份")
    cityarea = models.ForeignKey("Area", related_name="cityarea", on_delete=models.CASCADE, verbose_name="地区")
    hospitallv = models.ForeignKey("HospitalLv", on_delete=models.CASCADE, verbose_name="等级")
    hospitaltype = models.ManyToManyField("HospitalType", verbose_name="类型")
    thumb = models.ImageField(verbose_name='缩略图', default="thumbnail/824.png", upload_to='thumbnail')
    power = models.ManyToManyField("Power", verbose_name="重点类型")

    class Meta:
        verbose_name = "医院介绍文章"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Mail(models.Model):
    username = models.CharField(max_length=32, verbose_name="名字")
    userhead = models.TextField(verbose_name="头像地址")
    mail = models.TextField(verbose_name="感谢信")
    doctor = models.ForeignKey("Doctor", default=1, on_delete=models.CASCADE, verbose_name="医生")

    class Meta:
        verbose_name = "感谢信"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mail


class Doctor(models.Model):
    name = models.CharField(max_length=32, verbose_name="名字")
    choices = (
        (1, '男'), (2, '女')
    )
    gender = models.IntegerField(choices=choices, verbose_name="性别")
    area = models.CharField(max_length=32, verbose_name="地区")
    keshi = models.CharField(max_length=32, verbose_name="所属科室")
    zhiwei = models.CharField(max_length=32, verbose_name="职位")
    goodjob = models.CharField(max_length=100, verbose_name="擅长领域")
    title = models.CharField(max_length=100, verbose_name="荣誉称号")
    details = models.TextField(verbose_name="详细介绍")
    hospital = models.ForeignKey("Hospital", default=2, on_delete=models.CASCADE, verbose_name="所属医院")
    thumb = models.ImageField(verbose_name='缩略图', default="thumbnail/824.png", upload_to='thumbnail')
    power = models.ManyToManyField("Power", verbose_name="重点类型", null=True)

    class Meta:
        verbose_name = "医生详情"  # 在admin站点显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
