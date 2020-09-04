from django.db import models
from django.utils import timezone


# Create your models here.
# it should be in the section module, temp be here.


class UserInfoModel(models.Model):
    class Gender:
        CHOICE = (('m', "爷们"), ('f', "娘们"), ('u', "未知"))

    class Rank:
        CHOICE = (('normal', "大众"), ('vip', "会员"), ('svip', "超级会员"))

    username = models.CharField(verbose_name='name', max_length=32, null=False, blank=False, unique=True)
    password = models.CharField(verbose_name='password', max_length=32, null=False, blank=False)
    nickname = models.CharField(verbose_name='nickname', max_length=64, null=False, blank=False)
    age = models.IntegerField(verbose_name='nickname', default=0)
    gender = models.CharField(verbose_name='gender', default='u', max_length=1, choices=Gender.CHOICE)
    rank = models.CharField(verbose_name='rank', default='normal', max_length=16, choices=Rank.CHOICE)
    friends = models.ManyToManyField('self')
    last_modify = models.DateTimeField(verbose_name='last modify time', auto_now=True)
    created_time = models.DateTimeField(verbose_name='create time', auto_now_add=True, default=timezone.now)


class Role(models.Model):
    class UserRole:
        CHOICE = (('normal', "普通用户"), ('manger', "管理员"), ('sectioner', "版主"), ('admin', "官方管理员"))

    class Section:
        CHOICE = (('none', "孤苦伶仃"), ('coding', "编程"), ('language', "语言"), ('history', "历史"))

    user = models.ForeignKey(UserInfoModel, on_delete=models.CASCADE, related_name='user_role')
    role = models.CharField(verbose_name='user role', choices=UserRole.CHOICE, default='normal', max_length=16)
    section = models.CharField(verbose_name='section', choices=Section.CHOICE, default='none', max_length=16)
