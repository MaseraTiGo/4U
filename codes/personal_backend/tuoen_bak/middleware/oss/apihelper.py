# coding=UTF-8

'''
Created on 2016年8月24日

@author: Administrator
'''

# import python standard package

# import thread package
# import oss2

# import my project package


access_key_id = 'OYkUtypSPFejiEgl'
access_key_secret = 'rrbXcHNX9j1PtNwOBnEOacQY8FN896'

endpoint = "http://oss-cn-hangzhou.aliyuncs.com"

class OSSAPI(object):
    
    def __init__(self):
        self.auth = None
        # self.auth = oss2.Auth(access_key_id, access_key_secret)
        self._register = {}
        
    def get_bucket(self, bucket_name):
        if bucket_name not in self._register:
            # bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
            # self._register[bucket_name] = bucket
            self._register[bucket_name] = None
        return self._register[bucket_name]
    
    def put_object(self, store_name, content, bucket_name):
        backet = self.get_bucket(bucket_name)
        if backet:
            return 'http://www.baidu.com'
            result = backet.put_object(store_name, content)
            return result.resp.response.url
        raise Exception("backet error for oss")

if __name__ == "__main__":
    oss = OSSAPI()
    bucket_name = 'test-tuoen'
    store_name = '哈哈.jpg'
    with open('d:\\哈哈.jpg', 'rb') as f:
        url = oss.put_object(store_name, f, bucket_name)
        print(url)
    
