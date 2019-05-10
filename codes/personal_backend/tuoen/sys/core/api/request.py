# coding=UTF-8

from tuoen.sys.core.field.adapter import AdapterField, AdapterFieldSet


class RequestField(AdapterField):

    def __init__(self, field_cls, is_need = True, *args, **kwargs):
        super(RequestField, self).__init__(field_cls, *args, **kwargs)
        self._is_need = is_need

    def is_need(self):
        return self._is_need

    def execute(self, value, *args, **kwargs):
        return self.get_field().parse(value, *args, **kwargs)


class RequestFieldSet(AdapterFieldSet):

    _field_cls = RequestField
