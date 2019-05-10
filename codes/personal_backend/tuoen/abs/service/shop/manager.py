# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import *

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from model.store.model_shop import Channel, Shop, Goods
from model.store.model_measure_shop import MeasureShop


class ChannelServer(object):

    @classmethod
    def generate(cls, **attr):
        """创建渠道"""

        Channel.create(**attr)

    @classmethod
    def get(cls, channel_id):
        """获取渠道详情"""

        channel = Channel.get_byid(channel_id)
        if channel is None:
            raise BusinessError("渠道不存在")
        return channel

    @classmethod
    def search(cls, current_page, **search_info):
        """查询渠道列表"""

        channel_qs = Channel.query(**search_info)

        channel_qs = channel_qs.order_by("-create_time")
        return Splitor(current_page, channel_qs)

    @classmethod
    def search_all(cls, **search_info):
       """查询所有店铺渠道列表"""

       return Channel.query(**search_info).order_by("-create_time")

    @classmethod
    def is_name_exist(cls, name, channel = None):
        """判断渠道名称是否存在"""

        channel_qs = Channel.search(name = name)

        if channel is not None:
            channel_qs = channel_qs.filter(~Q(id = channel.id))

        if channel_qs.count() > 0:
            raise BusinessError("该名称已存在")
        return True

    @classmethod
    def update(cls, channel, **attrs):
        """编辑渠道"""

        channel.update(**attrs)
        return True

    @classmethod
    def remove(cls, channel_id):
        """移除渠道"""

        channel = cls.get(channel_id)
        shop_qs = ShopServer.search_all(channel = channel)
        if shop_qs.count() > 0:
            raise BusinessError("该渠道下存在店铺，无法删除")
        channel.delete()
        return True

    @classmethod
    def match(cls, keyword, size = 5):
        """匹配店铺渠道列表"""

        return Channel.query(name = keyword).order_by('-create_time')[:size]

    @classmethod
    def hung_channel_forshops(cls, measure_shop_list):
        """给店铺绩效挂载店铺渠道"""

        channel_id_list = [measure_shop.shop.channel_id \
                            for measure_shop in measure_shop_list]

        channel_mapping = {channel.id: channel for channel in \
                            Channel.search(id__in = channel_id_list)}

        for measure_shop in measure_shop_list:
            if measure_shop.shop.channel_id is not None:
                channel = channel_mapping.get(measure_shop.shop.channel_id)
                measure_shop.channel = channel
            else:
                measure_shop.channel = None

        return measure_shop_list


class ShopServer(object):

    @classmethod
    def generate(cls, **attr):
        """创建店铺"""
        Shop.create(**attr)

    @classmethod
    def get(cls, shop_id):
        """获取店铺详情"""
        shop = Shop.get_byid(shop_id)
        if shop is None:
            raise BusinessError("店铺不存在")
        return shop

    @classmethod
    def search(cls, current_page, **search_info):
        """查询店铺列表"""
        if "channel_id" in search_info:
            channel = ChannelServer.get(search_info["channel_id"])
            search_info.update({"channel":channel})

        shop_qs = Shop.query(**search_info)
        if "name" in search_info:
            keyword = search_info.pop('name')
            shop_qs = shop_qs.filter(Q(name__contains = keyword) \
                        | Q(channel__name__contains = keyword))

        shop_qs = shop_qs.order_by("-create_time")
        return Splitor(current_page, shop_qs)

    @classmethod
    def search_all(cls, **search_info):
       """查询所有店铺列表"""

       return Shop.query(**search_info).order_by("-create_time")

    @classmethod
    def get_byname(cls, name):
        """根据名称查询店铺"""

        return Shop.get_shop_buyname(name)

    @classmethod
    def is_name_exist(cls, name, shop = None):
        """判断渠道名称是否存在"""

        shop_qs = Shop.search(name = name)

        if shop is not None:
            shop_qs = shop_qs.filter(~Q(id = shop.id))

        if shop_qs.count() > 0:
            raise BusinessError("该名称已存在")
        return True

    @classmethod
    def update(cls, shop, **attrs):
        """编辑店铺"""

        shop.update(**attrs)
        return True

    @classmethod
    def remove(cls, shop_id):
        """移除店铺"""
        shop = cls.get(shop_id)

        measure_shop_qs = MeasureShop.search(shop = shop)
        if measure_shop_qs.count() > 0:
            raise BusinessError("该店铺存在绩效无法删除")
        # 判断是否存在商品
        shop.delete()
        return True

    @classmethod
    def match(cls, keyword, size = 5):
        """匹配店铺列表"""
        return Shop.query(name = keyword).order_by('-create_time')[:size]

    @classmethod
    def hung_shopnum_bychannel(cls, channel_list):
        """挂载店铺数量"""

        channel_mapping = {}
        for channel in channel_list:
            channel.shop_num = 0
            channel_mapping[channel.id] = channel

        notifications = Shop.objects.all().values('channel_id').annotate(count = Count('channel_id'))

        for item in notifications:
            if item["channel_id"] in channel_mapping:
                channel_mapping[item["channel_id"]].shop_num = item["count"]

        return channel_list


class GoodsServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询商品列表"""

        goods_qs = cls.search_qs(**search_info)

        return Splitor(current_page, goods_qs)

    @classmethod
    def search_all(cls, **search_info):
        """查询所有商品列表"""

        return cls.search_qs(**search_info)

    @classmethod
    def search_qs(cls, **search_info):
        goods_qs = Goods.query(**search_info)
        goods_qs = goods_qs.order_by("-create_time")
        return goods_qs

    @classmethod
    def match(cls, keyword, size = 5):
        """匹配商品列表"""

        return Goods.query(name = keyword).order_by('-create_time')[:size]

    @classmethod
    def get(cls, goods_id):
        """获取商品详情"""
        goods = Goods.get_byid(goods_id)

        return goods
