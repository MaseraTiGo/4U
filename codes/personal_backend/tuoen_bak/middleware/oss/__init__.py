# coding=UTF-8

import time
import collections

from settings import DEBUG, TEST
from .apihelper import OSSAPI


class OSSRegister(object):
    
    TEST_OSS = "test-tuoen"
    CRM_OSS = "tuoen-crm"
    APK_OSS = "tuoen-apk"
    COMMON_OSS = "tuoen-common"
    SUPPORT_OSS = "tuoen-support"
    SAFE_OSS = "tuoen-safe"
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(OSSRegister, cls).__new__(cls, *args, **kwargs)
            cls._register = collections.OrderedDict()
        return cls._instance

    def register(self, entity):
        if entity.name not in self._register:
            self._register[entity.name] = entity
        else:
            raise Exception("The {} bucket have register.".format(entity.name))
    
    def get_entity(self, module):
        if module in self._register:
            return self._register[module]
        raise Exception("The {} module is not exist for oss.".format(module))
    
    def get_all_entity(self):
        return self._register.values() 

    def get_bucket(self, module):
        return self.get_entity(module).bucket
    
class OSSHelper(object):
    
    def __init__(self):
        self.register =  OSSRegister()
        self.api =  OSSAPI()
    
    def get_store_file_name(self, store_name, store_module):
        name_fmt = "{module}-{file_name}-{timestamp}"
        suffix_fmt = ".{suffix}"
        split_list = store_name.split('.', -1)
        
        file_name = name_fmt.format(module = store_module, \
                file_name = split_list[0], timestamp = int(time.time()))
        if len(split_list) > 1:
            file_name += suffix_fmt.format(suffix = split_list[1])
            
        return file_name
    
    def put_object(self, file, store_module):
        store_name = self.get_store_file_name(file.name, store_module)
        return self.put_object_byIO(store_name, file, store_module)
    
    def put_object_byIO(self, store_name, file, store_module):
        bucket_name = self.register.get_bucket(store_module)
        bucket_name = OSSRegister.TEST_OSS if DEBUG or TEST else bucket_name
        return self.api.put_object(store_name, file, bucket_name)
    
class OSSEntity(object):
    
    def __init__(self, name, bucket, desc, is_show = True):
        self.name = name
        self.bucket = bucket
        self.desc = desc
        self.is_show = is_show
         
oss_helper = OSSHelper()
oss_register = OSSRegister()

oss_list = [
    OSSEntity("nick", OSSRegister.COMMON_OSS, "用于app头像存储类型, 如：社区头像"),
    OSSEntity("post", OSSRegister.COMMON_OSS, "用于社区交流, 如：创建帖子的图片"),
    
    OSSEntity("article", OSSRegister.SUPPORT_OSS, "用于crm后台进行文章维护, 如：会诊须知，会诊流程等图片素材"),
    OSSEntity("goods", OSSRegister.SUPPORT_OSS, "用于crm后台维护商品, 如：商品图片，商品详情"),
    OSSEntity("drug", OSSRegister.SUPPORT_OSS, "用于crm后台维护药品, 如：药品图片，药品详情"),
    
    OSSEntity("detection", OSSRegister.SAFE_OSS, "用于支持现网检测配置项的文件类型，如：检测报告pdf"),
    OSSEntity("consultation", OSSRegister.SAFE_OSS, "用于支持现网会诊置项的文件类型，如：会诊申请单"),
    OSSEntity("role", OSSRegister.SAFE_OSS, "用于存储用户真实信息, 如：用户真实头像，用户名片信息等"),
    OSSEntity("document", OSSRegister.SAFE_OSS, "用于用户的重要信息存档, 如：医生学术讨论文档"),
    OSSEntity("case", OSSRegister.SAFE_OSS, "用于支持现网病例图片上传，如：住院记录"),
    OSSEntity("treat", OSSRegister.SAFE_OSS, "用于支持医生治疗信息存档，如：治疗思路"),
    OSSEntity("prescription", OSSRegister.SAFE_OSS, "用于支持用户处方图片存档，如：需求处方，代取处方，订单处方"),
    
    OSSEntity("test", OSSRegister.TEST_OSS, "用于测试环境", False),
]

for oss_entity in oss_list:
    oss_register.register(oss_entity)
