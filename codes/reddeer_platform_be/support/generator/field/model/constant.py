# coding=UTF-8

import random
from support.generator.field.base import BaseHelper


class AccountStatusHelper(BaseHelper):

    def calc(self):
        from model.store.model_account import BaseAccount
        return random.choice(BaseAccount.Status.choices)[0]
