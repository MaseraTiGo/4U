# coding=UTF-8

from tuoen.sys.core.service.base import BaseAPIService


class FileService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "文件服务"

    @classmethod
    def get_desc(self):
        return "提供文件上传服务"

    @classmethod
    def get_flag(cls):
        return "file"


file_service = FileService()
from tuoen.agile.agent_apis.file import Upload

file_service.add(Upload)
