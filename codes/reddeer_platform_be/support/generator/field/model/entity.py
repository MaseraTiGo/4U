# coding=UTF-8

import random
from support.generator.field.base import BaseHelper


class PlatformAccountHelper(BaseHelper):

    def calc(self, has_none=False):
        if not hasattr(self, '_enumerate'):
            from model.store.model_account import PlatformAccount
            _enumerate = []
            for platform_account in PlatformAccount.search(id__gt=1):
                _enumerate.append(platform_account)

        select_enum = _enumerate.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)
