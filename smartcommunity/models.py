from django.db import models


# Create your models here.
### 开启app广告页表模型 ###
class Welcome(models.Model):
    # upload_to图片上传后，放到media文件夹下的welcome文件夹下
    # 必须安装pillow模块 pip3 install pillow
    img = models.ImageField(upload_to="welcome", default="/welcome/slash.png")
    order = models.IntegerField()
    # 这个字段以后不用传，会自动把上传的图片的时间存到数据库
    create_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "欢迎表"

    def __str__(self):
        return str(self.img)


# 轮播图表
class Banner(models.Model):
    img = models.ImageField(upload_to='banner', default='banner1.png', verbose_name='图片')
    order = models.IntegerField(verbose_name='顺序')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name_plural = '轮播图'

    def __str__(self):
        return str(self.img)


# 通知表
class Notice(models.Model):
    title = models.CharField(max_length=64, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    img = models.ImageField(upload_to='notice', default='notice.png', verbose_name='公告图片')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '公告表'

    def __str__(self):
        return self.title


# 采集表---collection
class Collection(models.Model):
    name = models.CharField(max_length=32, verbose_name='采集人员姓名')
    # 做为人脸识别的id号
    name_pinyin = models.CharField(max_length=32, verbose_name='姓名拼音', null=True)
    avatar = models.ImageField(upload_to='collection/%Y/%m/%d/', default='default.png', verbose_name='头像')
    create_time = models.DateTimeField(auto_now=True, verbose_name='采集时间')
    # face_token---->人脸识别的token唯一码
    # 区域外键关联
    area = models.ForeignKey(to='Area', null=True, verbose_name='网格区域', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '采集表'

    def __str__(self):
        return self.name


# 区域表---area
class Area(models.Model):
    name = models.CharField(max_length=32, verbose_name='网格区域名')
    desc = models.CharField(max_length=32, verbose_name='网格简称')
    # 跟用户一对多---》一个网格员，可以采集多个网格
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE, null=True, verbose_name="负责用户")

    class Meta:
        verbose_name_plural = '区域表'

    def __str__(self):
        return self.name


# 用户表--UserInfo
class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    avatar = models.FileField(verbose_name="头像", max_length=128, upload_to='avatar')
    create_date = models.DateField(verbose_name="日期", auto_now_add=True)
    score = models.IntegerField(verbose_name="积分", default=0)

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.name
