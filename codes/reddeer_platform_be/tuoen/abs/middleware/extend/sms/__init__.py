# coding=UTF-8
import json

from tuoen.abs.middleware.extend.sms.platform import sms_platform_repo
from tuoen.sys.utils.cache.redis import redis
from tuoen.sys.utils.common.single import Single


class SmsMiddleware(Single):
    @staticmethod
    def get_company_obj(label):
        return sms_platform_repo.all_controllers.get(label)

    @staticmethod
    def get_company_mapping():
        return sms_platform_repo.all_controllers

    @staticmethod
    def get_template(label):
        return sms_platform_repo.all_templates_mapping.get(label)

    @staticmethod
    def get_template_mapping():
        return sms_platform_repo.all_templates_mapping

    def send(self, label, phone, template_id, template, **kwargs):
        return self.get_company_obj(label).send(phone, template_id, template, **kwargs)

    @classmethod
    def get_label_is_open(cls, label):
        """短信平台开关"""
        from tuoen.abs.middleware.config import config_middleware
        return config_middleware.get_value(label, 'is_open')

    @classmethod
    def get_scene_is_open(cls, scene):
        """短信场景开关 """
        from tuoen.abs.middleware.config import config_middleware
        return config_middleware.get_value('common_sms', scene + '_is_open')

    sms_redis_key = 'sms_label_customer_num'

    @classmethod
    def set_sms_label(cls):
        sms_label_mapping = redis.get_new(cls.sms_redis_key)
        if sms_label_mapping and json.loads(sms_label_mapping):
            sms_label_mapping = json.loads(sms_label_mapping)
        else:
            sms_label_mapping = cls.loading_sms_label()
        sms_label_list = list(sms_label_mapping.values())
        sms_label_list.sort(key=lambda x: x['number'], reverse=False)
        flag = False
        sms_label = None
        for item in sms_label_list:
            sms_label = item['label']
            is_open = cls.get_label_is_open(sms_label)
            if is_open:
                flag = True
                sms_label_mapping[sms_label]['number'] += 1
                break
        redis.set(cls.sms_redis_key, json.dumps(sms_label_mapping))
        return sms_label if flag else 'haoservice_sms'

    # @classmethod
    # def loading_sms_label(cls):
    #     label_list = list(sms_middleware.get_company_mapping().keys())
    #     mapping = {}
    #     for item in label_list:
    #         number = Customer.objects.filter(sms_label=item).count()
    #         mapping.update({item: {'number': number, 'label': item}})
    #     redis.set(cls.sms_redis_key, json.dumps(mapping))
    #     return mapping


sms_middleware = SmsMiddleware()
