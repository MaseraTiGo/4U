# coding=UTF-8

from model.models import AgentRole


class LoaderHelper(object):

    @classmethod
    def loading(cls):
        return AgentRole.query().order_by('create_time')
