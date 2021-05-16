# coding=UTF-8

from urllib import parse
from tuoen.agile.agent_apis.server import ServerAuthorizedApi
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.field.base import CharField, FileField, ListField, DictField
from abs.middleware.file import file_middleware


class Upload(ServerAuthorizedApi):
    """上传图片"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc="上传文件")
    request.store_type = RequestField(CharField, desc="上传至文件夹")

    response = with_metaclass(ResponseFieldSet)
    response.file_paths = ResponseField(ListField, desc='文件路径列表', fmt=CharField(desc='url'))
    response.file_infos = ResponseField(ListField, desc='pic info', fmt=ListField(
        desc='文件信息', fmt=CharField(desc='信息'), is_required=False))

    @classmethod
    def get_desc(cls):
        return "上传文件"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        path_list = []
        extra_infos = []
        for name, f in request._upload_files.items():
            name = str(f)
            url = file_middleware.save_oss(name, f, store_type=request.store_type)
            path_list.append(url)
            extra_infos.append([name, f.size])
        #     path = file_middleware.save(
        #         name,
        #         f,
        #         request.store_type,
        #         "local"
        #     )
        #     path_list.append(parse.unquote(path))
        #
        # new_path_list = []
        # from django.conf import settings
        # domain = settings.HOST_DOMAIN_OWN
        #
        # for path in path_list:
        #     new_path_list.append(domain+path)
        return path_list, extra_infos

    def fill(self, response, path_list, extra_infos):
        response.file_paths = path_list
        response.file_infos = extra_infos
        return response
