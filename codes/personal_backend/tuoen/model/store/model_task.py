# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class GroupStatus(object):
    INIT = "init"
    GENERATTING = "generatting"
    GENERATED = "generated"
    EXECUTTING = "executting"
    FINISHED = "finished"
    CANCEL = "cancel"
    CHOICES = ((INIT, '初始化'), (GENERATTING, "任务生成中"), (GENERATED, "任务生成完成"), \
               (EXECUTTING, "任务执行中"), (FINISHED, "任务执行完成"), (CANCEL, "任务取消"))


class TaskGroup(BaseModel):
    name = CharField(verbose_name="任务组名称", max_length=64, default="")
    exec_cls = CharField(verbose_name="任务组执行类", max_length=128, default="")
    exec_parms = TextField(verbose_name="任务组执行参数", default="")
    status = CharField(verbose_name="任务组整体执行状态", choices=GroupStatus.CHOICES, \
                       max_length=32, default=GroupStatus.INIT)
    reason = TextField(verbose_name="任务取消原因", default="")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    def is_init(self):
        return self.status == GroupStatus.INIT

    def is_generatting(self):
        return self.status == GroupStatus.GENERATTING

    def is_generated(self):
        return self.status == GroupStatus.GENERATED

    def is_executting(self):
        return self.status == GroupStatus.EXECUTTING

    def is_finished(self):
        return self.status == GroupStatus.FINISHED

    def is_cancel(self):
        return self.status == GroupStatus.CANCEL

    def generatting(self):
        return self.update(status=GroupStatus.GENERATTING)

    def generated(self):
        return self.update(status=GroupStatus.GENERATED)

    def executting(self):
        return self.update(status=GroupStatus.EXECUTTING)

    def finished(self):
        return self.update(status=GroupStatus.FINISHED)

    def cancel(self):
        return self.update(status=GroupStatus.CANCEL)

    def get_undone_tasks(self):
        tasks = Task.query_undone_tasks(self)
        return tasks

    @classmethod
    def query_unexec_task_group(cls, exec_cls):
        try:
            return cls.query(exec_cls=exec_cls).filter(status__in=[GroupStatus.INIT, \
                            GroupStatus.GENERATED, GroupStatus.EXECUTTING]).\
                                order_by('-create_time')[0]
        except:
            return None


class TaskStatus(object):
    INIT = "init"
    EXECUTTING = "executting"
    FINISHED = "finished"
    FAILED = "failed"
    CANCEL = "cancel"
    CHOICES = ((INIT, '初始化'), (EXECUTTING, "任务执行中"), (FINISHED, "任务执行完成"),\
               (FAILED, "任务失败"), (CANCEL, "任务取消"))


class Task(BaseModel):
    name = CharField(verbose_name="任务名称", unique=True, max_length=64)
    group = ForeignKey(TaskGroup, on_delete=CASCADE)
    exec_parms = TextField(verbose_name="执行参数", default="")
    status = CharField(verbose_name="任务执行状态", choices=TaskStatus.CHOICES, \
                       max_length=32, default=TaskStatus.INIT)
    reason = TextField(verbose_name="任务失败原因", default="")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def query_undone_tasks(cls, group):
        return cls.query(group=group, status=TaskStatus.INIT)

    def is_init(self):
        return self.status == TaskStatus.INIT

    def is_executting(self):
        return self.status == TaskStatus.EXECUTTING

    def is_finished(self):
        return self.status == TaskStatus.FINISHED

    def is_failed(self, reason):
        return self.status == TaskStatus.FAILED

    def is_cancel(self):
        return self.status == TaskStatus.CANCEL

    def executting(self):
        return self.update(status=TaskStatus.EXECUTTING)

    def finished(self):
        return self.update(status=TaskStatus.FINISHED)

    def failed(self, reason):
        return self.update(status=TaskStatus.FAILED)

    def cancel(self):
        return self.update(status=TaskStatus.CANCEL)
