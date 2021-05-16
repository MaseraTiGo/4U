# coding=UTF-8
import json
import random
import string

from model.store.model_sms import Sms, StatusTypes
from tuoen.abs.middleware.config import config_middleware
from tuoen.abs.middleware.extend.sms import sms_middleware
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.cache.redis import redis


class CodeHelper(object):
    _verify_key = '{phone}_{code_type}'

    def __init__(self, template, phone, code_type):
        self.template = template
        self.phone = phone
        self.code_type = code_type
        self._key = self._verify_key.format(phone=self.phone, code_type=self.code_type)

    def generate_code(self):
        if self.code_type == 'agent_invite_code':
            letter_str = string.ascii_uppercase
            code = ''
            for item in range(0, 6):
                code += random.choice(letter_str)
        else:
            code = str(random.randint(100000, 999999))
        return code

    def get_verify_code(self):
        try:
            return redis.get(self._key)
        except Exception as e:
            return None

    def set_verify_code(self, verify_code):
        expire_time = 1800
        cur_expire_time = redis.ttl(self._key)
        if cur_expire_time and expire_time - cur_expire_time < 120:
            raise BusinessError('请不要在两分钟内重复获取验证码')
        return redis.set(self._key, verify_code, ex=expire_time)

    def check(self, code):
        verify_code = self.get_verify_code()
        if not verify_code or verify_code.lower() != code.lower():
            return False
        redis.delete(self._key)
        return True

    def send(self, company_obj, source_type):
        sign_name = company_obj.get_sign_name()
        code = self.generate_code()
        self.set_verify_code(code)
        template_id = config_middleware.get_value(company_obj.label, self.template.label)
        result = company_obj.send(self.phone, template_id, self.template, sign_name, code=code)
        status = StatusTypes.FAIL
        flag = False
        if result:
            status = StatusTypes.SUCCESS
            flag = True
        Sms.create(phone=self.phone, template_id=template_id, template_label=self.template.label,
                   label=company_obj.label, \
                   param=json.dumps(self.template.get_params(code)),
                   content='【' + sign_name + '】' + self.template.content, \
                   unique_no='', scene=self.code_type, status=status, source_type=source_type)
        return flag


class MessageHelper(object):

    def __init__(self, template, phone, unique_no, source_type):
        self.template = template
        self.phone = phone
        self.unique_no = unique_no
        self.source_type = source_type

    def send(self, company_label, **kwargs):
        template_id = config_middleware.get_value(company_label, self.template.label)
        company_obj = sms_middleware.get_company_obj(company_label)
        sign_name = company_obj.get_sign_name()
        result = company_obj.send(self.phone, template_id, self.template, sign_name, **kwargs)
        status = StatusTypes.FAIL
        flag = False
        if result:
            status = StatusTypes.SUCCESS
            flag = True
        Sms.create(phone=self.phone, template_id=template_id, template_label=self.template.label, label=company_label, \
                   param=json.dumps(self.template.get_params(**kwargs)),
                   content='【' + sign_name + '】' + self.template.content, \
                   unique_no=self.unique_no, scene=self.template.label, status=status, source_type=self.source_type)
        return flag
