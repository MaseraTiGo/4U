# coding=UTF-8

import oss2

# endpoint = "http://oss-cn-hangzhou.aliyuncs.com"
endpoint = "http://oss-cn-beijing.aliyuncs.com"


class OSSAPI(object):

    def __init__(self):
        self._register = {}

    @staticmethod
    def get_access_key_id():
        return 'LTAI4GJ4nsX38kR6BeTYA19X'

    @staticmethod
    def get_access_key_secret():
        return 'des3OnuwdsdnHQ0GPkbBcual3sQVTW'

    def _get_auth(self):
        s_auth = oss2.Auth(self.get_access_key_id(),
                           self.get_access_key_secret())
        return s_auth

    def get_bucket(self, bucket_name):
        if bucket_name not in self._register:
            bucket = oss2.Bucket(self._get_auth(), endpoint, bucket_name)
            self._register[bucket_name] = bucket
            # self._register[bucket_name] = None
        return self._register[bucket_name]

    def put_object(self, store_name, content, bucket_name):
        bucket = self.get_bucket(bucket_name)
        if bucket:
            result = bucket.put_object(store_name, content)
            return result.resp.response.url
        raise Exception("bucket error for oss")


oss = OSSAPI()
