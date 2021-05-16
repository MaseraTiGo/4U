# coding=UTF-8

from model.store.model_config import Config
from tuoen.abs.middleware.extend.sms.config import sms_platform_config_repo


class LoaderHelper(object):

    def __init__(self):
        self.data = {}
        self.get_config_data()

    def set_by_using_platforms(self):
        for platform in sms_platform_config_repo.all_platform_configs:
            self.set_key(*platform.platform_classify)
            for key, ex_args in platform.config_details_mapping.items():
                self.set_value(*key, **ex_args)

    @classmethod
    def generate(cls, **attr):
        config = Config.create(**attr)
        if config is not None:
            return config
        return None

    @classmethod
    def loading(cls, **search_info):
        config_list = list(Config.objects.filter(**search_info))
        for config in config_list:
            config.value_type = "text"
            config.option = []
            if config.type in LoaderHelper().data and config.key in LoaderHelper().data[config.type]['data']:
                config.value_type = LoaderHelper().data[config.type]['data'][config.key]["type"]
                config.option = LoaderHelper().data[config.type]['data'][config.key]["option"]
        return config_list

    @classmethod
    def get_config(cls, type, key):
        config_qs = Config.objects.filter(type=type, key=key)
        if config_qs:
            return config_qs[0]
        return None

    @classmethod
    def generate_config(cls, **attrs):
        return Config.create(**attrs)

    def set_key(self, key, desc):
        self.data.update({key: {'type_desc': desc, 'data': {}}})

    def set_value(self, key, value_key, name, default='', type='text', option=[]):
        self.data[key]['data'].update({value_key: {'name': name, 'value': default, 'type': type, 'option': option}})

    def get_config_data(self):
        # just for exhibiting usage. shall delete in production env.
        self.set_key('sample4show', '展示用例')
        self.set_value('sample4show', 'ironman', '铁皮人', default='yes', type='select', option=['yes', 'no'])
        self.set_value('sample4show', 'hulk', '绿色的大汉')
        # just for exhibiting usage. shall delete in production env.

        self.set_by_using_platforms()
