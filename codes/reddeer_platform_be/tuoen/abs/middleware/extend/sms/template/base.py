# coding=UTF-8


class TemplateBase(object):

    @property
    def label(self):
        return self.get_label()

    @property
    def name(self):
        return self.get_name()

    @property
    def content(self):
        return self.get_content()

    def get_label(self):
        raise NotImplementedError("server need to implement get_label function")

    def get_name(self):
        raise NotImplementedError("server need to implement get_name function")

    def get_params(self, *args, **kwargs):
        raise NotImplementedError("server need to implement get_params function")

    def get_content(self):
        from tuoen.abs.middleware.config import config_middleware
        return config_middleware.get_value('common_sms', self.label + '_content')

    def verify_unique_no(self, *args, **kwargs):
        raise NotImplementedError("server need to implement get_params function")
