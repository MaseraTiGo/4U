# -*- coding: utf-8 -*-
# file_name       : signals.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/30 14:45

from django.db.models.signals import post_save
from django.dispatch import receiver
from BuyGoods.models_store.members import Users


@receiver(post_save, sender=Users)
def notification_register_email(sender, *args, **kwargs):
    print('signal test===========>', sender, args, kwargs, 'register fucking success')


def notification_register_email_test(sender, *args, **kwargs):
    print('*' * 23)
    print(args, kwargs)
    print('*' * 23)
