# coding=UTF-8

import json
import random
from support.init.base import BaseLoader


class ProductLoader(BaseLoader):

    def load(self):
        return [
            {
                'name': '大蓝牙',
                'alias': '大蓝牙',
                'introduction': '大蓝牙简介',
                'details': '大蓝牙详情',
                'rebate_money': 300000,
                'thumbnail': json.dumps([]),
                'images': json.dumps([]),
                'postage': 10000000,
            },
            {
                'name': '小蓝牙',
                'alias': '小蓝牙',
                'introduction': '小蓝牙简介',
                'details': '小蓝牙详情',
                'rebate_money': 100000,
                'thumbnail': json.dumps([]),
                'images': json.dumps([]),
                'postage': 10000000,
            },
        ]


class ProductModelLoader(BaseLoader):

    def load(self):
        return [
            {
                'name': 'MS-2',
                'product_name': '大蓝牙',
                'rate': '0.7%+2',
                'remark':'售卖 0.54-0.65之间 秒到费2-3元',
                'stock': 10000,
            },
            {
                'name': 'MF-1',
                'product_name': '大蓝牙',
                'rate': '0.7%+2',
                'remark':'售卖 0.54-0.55之间 秒到费3元',
                'stock': 10000,
            },
            {
                'name': 'MF-2',
                'product_name': '大蓝牙',
                'rate': '0.7%+2',
                'remark':'售卖 0.54-0.55之间 秒到费3元',
                'stock': 10000,
            },
            {
                'name': 'BS-1',
                'product_name': '小蓝牙',
                'rate': '0.7%+2',
                'remark':'售卖 0.54-0.65之间 秒到费2-3元',
                'stock': 10000,
            },
            {
                'name': 'BD-1',
                'product_name': '小蓝牙',
                'rate': '0.7%+2',
                'remark':'售卖 0.54-0.65之间 秒到费2-3元',
                'stock': 10000,
            },
        ]


class ChannelLoader(BaseLoader):

    def load(self):
        return [
            {
                'name': '系统渠道',
                'freight':1000000,
                'single_repair_money': 0,
                'single_point_money': 0,
                'remark': '系统渠道',
            }
        ]


class ShopLoader(BaseLoader):

    def load(self):
        return [
            {
                'channel_name': '系统渠道',
                'name': '系统店铺',
                'single_point_money': 0,
                'single_repair_money': 0,
                'is_distribution': False,
                'remark': '系统店铺',
            },
        ]


class GoodsLoader(BaseLoader):

    def load(self):
        return [
            {
                'shop_name': '系统店铺',
                'product_name': '',
                'code': '0000000',
                'price': 1000000,
                'rate': "0.7%+2",
                'name': '系统商品',
                'alias': '系统商品',
                'introduction': '系统商品-简介',
                'details': '系统商品-详情',
                'thumbnail': json.dumps([]),
                'images': json.dumps([]),
                'postage': 1000000,
                're_num': 1000000,
            }
        ]
