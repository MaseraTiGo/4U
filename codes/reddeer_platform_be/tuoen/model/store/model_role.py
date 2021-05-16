from django.db.models import *

from model import AGENT_PREFIX, PLATFORM_PREFIX
from model.base import BaseModel
from model.fields import VirtualForeignKey
from model.store.model_company import Company


class MyManager(Manager):
    def get_queryset(self):
        super_qs = super().get_queryset()
        return super_qs.exclude(status=RoleBase.Status.DELETE)


class RoleBase(BaseModel):
    class Status(IntegerChoices):
        DISABLE = 0
        ENABLE = 1
        DELETE = 2

        # STATUS_CHOICES = [(ENABLE, '启用'), (DISABLE, "停用")]

    name = CharField(verbose_name="角色名称", max_length=32, default="")

    rules = JSONField(verbose_name="角色对应权限", default=list)
    describe = CharField(verbose_name="描述", default="", max_length=32)
    status = IntegerField(
        verbose_name="状态:DISABLE = 0 ENABLE = 1 DELETE = 2 [(ENABLE, 启用), (DISABLE, 停用), (DELETE, 删除)]",
        choices=Status.choices, default=Status.ENABLE)

    objects = MyManager()

    class Meta:
        abstract = True


class AgentRole(RoleBase):
    company = VirtualForeignKey(Company, on_delete=CASCADE, related_name='company_roles')

    class Meta:
        db_table = AGENT_PREFIX + 'role'


class PlatformRole(RoleBase):
    class Meta:
        db_table = PLATFORM_PREFIX + 'role'
