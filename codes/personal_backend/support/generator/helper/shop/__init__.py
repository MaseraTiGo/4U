# coding=UTF-8

import json
import random
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.log.base import logger
from model.store.model_shop import Channel, Shop, Goods
from support.generator.base import BaseGenerator
from support.generator.helper.product import ProductGenerator, ProductModelGenerator


class ChannelGenerator(BaseGenerator):

    def __init__(self, channel_info):
        super(ChannelGenerator, self).__init__()
        self._channel_infos = self.init(channel_info)

    def get_create_list(self, result_mapping):
        return self._channel_infos

    def create(self, channel_info, result_mapping):
        channel_qs = Channel.query().filter(name = channel_info.name)
        if channel_qs.count():
            channel = channel_qs[0]
        else:
            channel = Channel.create(**channel_info)
        return channel

    def delete(self):
        print('======================>>> delete channel <======================')
        return None


class ShopGenerator(BaseGenerator):

    def __init__(self, shop_info):
        super(ShopGenerator, self).__init__()
        self._shop_infos = self.init(shop_info)

    def get_create_list(self, result_mapping):
        channel_list = result_mapping.get(ChannelGenerator.get_key())
        channel_mapping = {channel.name: channel for channel in channel_list}

        for shop_info in self._shop_infos:
            channel = channel_mapping.get(shop_info.channel_name)
            shop_info.channel = channel

        return self._shop_infos

    def create(self, shop_info, result_mapping):
        shop_qs = Shop.query().filter(channel = shop_info.channel, \
                                    name = shop_info.name)
        if shop_qs.count():
            shop = shop_qs[0]
        else:
            shop = Shop.create(**shop_info)
        return shop

    def delete(self):
        print('======================>>> delete shop <======================')
        return None


class GoodsGenerator(BaseGenerator):

    def __init__(self, goods_info):
        super(GoodsGenerator, self).__init__()
        self._goods_infos = self.init(goods_info)

    def get_create_list(self, result_mapping):
        shop_list = result_mapping.get(ShopGenerator.get_key())
        shop_mapping = {shop.name: shop for shop in shop_list}
        product_model_list = result_mapping.get(ProductModelGenerator.get_key())
        product_model = random.choice(product_model_list)

        for goods_info in self._goods_infos:
            goods_info.shop = shop_mapping.get(goods_info.shop_name)
            goods_info.product_model = product_model

        return self._goods_infos

    def create(self, goods_info, result_mapping):
        goods_qs = Goods.query().filter(shop = goods_info.shop, \
                                       name = goods_info.name)
        if goods_qs.count():
            goods = goods_qs[0]
        else:
            goods = Goods.create(**goods_info)
        return goods

    def delete(self):
        print('======================>>> delete goods <======================')
        return None
