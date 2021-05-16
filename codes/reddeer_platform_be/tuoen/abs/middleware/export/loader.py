# coding=UTF-8

import datetime
import json
import time

from django.db.models import *
from tuoen.sys.core.exception.business_error import BusinessError
from model.store.model_export import Export


class ExportHelper(object):

    @classmethod
    def create(cls, **attr):
        export = None
        export = Export.create(**attr)
        return export

    @classmethod
    def get(cls, export_id):
        export = Export.get_byid(export_id)
        if export is None:
            raise BusinessError("该下载连接不存在")
        return export

    @classmethod
    def get_new(cls, **search_info):
        export = None
        search_info.update({"create_time__gte": datetime.datetime.combine(datetime.datetime.now(), datetime.time.min)})
        export_qs = Export.search(**search_info).order_by("-create_time")
        if export_qs.count() > 0:
            export = export_qs[0]
        return export


export_helper = ExportHelper()
