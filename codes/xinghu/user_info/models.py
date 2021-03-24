import time
import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.common import CommonMiddleware


# Create your models here.
# it should be in the section module, temp be here.

class BaseModel(models.Model):
    last_modify = models.DateTimeField(verbose_name='last modify time', auto_now=True)
    created_time = models.DateTimeField(verbose_name='create time', auto_now_add=True)

    class Meta:
        abstract = True


class UserInfoModel(BaseModel):
    @property
    def nick_name(self):
        prefix = "anonymous"
        name = str(time.time())
        namespace = uuid.NAMESPACE_OID
        return prefix + str(uuid.uuid5(namespace, name)).split('-')[-1]

    class Rank:
        CHOICE = (('normal', "大众"), ('vip', "会员"), ('svip', "超级会员"))

    username = models.CharField(verbose_name='name', max_length=32, null=False, blank=False, unique=True)
    phone = models.CharField(verbose_name='phone', max_length=14, default='')
    password = models.CharField(verbose_name='password', max_length=32, null=False, blank=False)
    nickname = models.CharField(verbose_name='nickname', max_length=64, default='')
    rank = models.CharField(verbose_name='rank', default='normal', max_length=16, choices=Rank.CHOICE)
    friends = models.ManyToManyField('self')

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(self.password, password)


class UserDetailsModel(BaseModel):
    class Gender:
        CHOICE = (('m', "官人"), ('f', "佳人"), ('u', "神人"))

    class Diploma:
        CHOICE = (
            ('primary', "幼稚园"), ('junior', '小学'), ('senior', '高中'), ('bachelor', '本科'), ('ma', '硕士'), ('ph.d', '博士')
            , ('professor', '教授'), ('ac', '院士'), ('other', '其他'))

    user = models.OneToOneField(UserInfoModel, on_delete=models.CASCADE, related_name='user_query_detail')
    age = models.IntegerField(verbose_name='nickname', default=0)
    gender = models.CharField(verbose_name='gender', default='u', max_length=1, choices=Gender.CHOICE)
    address = models.CharField(verbose_name='address', default='', max_length=256)
    diploma = models.CharField(verbose_name='diploma', default='other', max_length=16, choices=Diploma.CHOICE)


class InterestModel(BaseModel):
    user = models.ForeignKey(UserInfoModel, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='user_query_interest', related_query_name='interest_query_user')
    interest = models.CharField(verbose_name='interest', max_length=64, default='', unique=True)


class RoleModel(BaseModel):
    class UserRole:
        CHOICE = (('normal', "普通用户"), ('manger', "管理员"), ('sectioner', "版主"), ('admin', "官方管理员"))

    class Section:
        CHOICE = (('none', "孤苦伶仃"), ('coding', "编程"), ('language', "语言"), ('history', "历史"))

    user = models.ForeignKey(UserInfoModel, on_delete=models.CASCADE, related_name='user_query_role',
                             related_query_name='role_query_user')
    role = models.CharField(verbose_name='user role', choices=UserRole.CHOICE, default='normal', max_length=16)
    section = models.CharField(verbose_name='section', choices=Section.CHOICE, default='none', max_length=16)

    class Meta:
        unique_together = ('user', 'role', 'section')
