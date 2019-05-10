# coding=UTF-8

import json
import random
import datetime
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.log.base import logger
from model.store.model_shop import Goods
from model.store.model_customer import Customer
from model.store.model_customer_chance import SaleChance
from model.store.model_order import Order, OrderItem, StatusTypes
from model.store.model_logistics import Logistics, LogisticsItem
from model.store.model_service import Service, ServiceItem
from support.generator.base import BaseGenerator
from support.simulate.tool.base.general import LogisticsNumberHelper, \
        LogisticsCompanyHelper
from support.simulate.tool.base.model import StaffHelper, EquipStatusHelper, \
        EquipmentModelHelper


class CustomerGenerator(BaseGenerator):

    def __init__(self, customer_info):
        super(CustomerGenerator, self).__init__()
        self._customer_infos = self.init(customer_info)

    def get_create_list(self, result_mapping):
        return self._customer_infos

    def create(self, customer_info, result_mapping):
        customer_qs = Customer.query().filter(phone = customer_info.phone)
        if customer_qs.count():
            customer = customer_qs[0]
        else:
            customer = Customer.create(**customer_info)
        return customer

    def delete(self):
        return None


class SaleChanceGenerator(BaseGenerator):

    def __init__(self, chance_info):
        super(SaleChanceGenerator, self).__init__()
        self._chance_infos = self.init(chance_info)

    def get_create_list(self, result_mapping):
        customer_list = result_mapping.get(CustomerGenerator.get_key())
        for chance in self._chance_infos:
            chance.customer = customer_list[0]
        return self._chance_infos

    def create(self, chance_info, result_mapping):
        chance_qs = SaleChance.query().filter(\
            customer = chance_info.customer,\
                goods = chance_info.goods,\
                    end_time__lt = datetime.datetime.now())
        if chance_qs.count():
            chance = chance_qs[0]
        else:
            chance = SaleChance.create(**chance_info)
        return chance

    def repair(self, obj, result_mapping):
        return obj

    def delete(self):
        return None


class OrderGenerator(BaseGenerator):

    def __init__(self, order_info):
        super(OrderGenerator, self).__init__()
        self._order_infos = self.init(order_info)

    def get_create_list(self, result_mapping):
        customer_list = result_mapping.get(CustomerGenerator.get_key())
        chance_list = result_mapping.get(SaleChanceGenerator.get_key())
        for order in self._order_infos:
            order.customer = random.choice(customer_list)
            order.shop = random.choice(chance_list).shop
            order.status = StatusTypes.SUBMIT
        return self._order_infos

    def create(self, order_info, result_mapping):
        order_qs = Order.query().filter(order_sn = order_info.order_sn)
        if order_qs.count():
            order = order_qs[0]
        else:
            order = Order.create(**order_info)
        return order

    def repair(self, order, result_mapping):
        chance_list = result_mapping.get(SaleChanceGenerator.get_key())
        chance = random.choice(chance_list)
        chance.order_count += 1
        try:
            order_ids = json.loads(chance.order_ids)
        except Exception as e:
            order_ids = []
        order_ids.append(order.id)
        chance.order_ids = json.dumps(order_ids)
        if chance.end_time < order.create_time:
            order.create_time = chance.end_time - datetime.timedelta(days = 2)
        chance.save()
        order._chance = chance
        return order

    def delete(self):
        return None


class OrderItemGenerator(BaseGenerator):

    def __init__(self, order_item_info):
        super(OrderItemGenerator, self).__init__()
        self._order_item_infos = self.init(order_item_info)

    def get_create_list(self, result_mapping):
        order_list = result_mapping.get(OrderGenerator.get_key())

        for order_item in self._order_item_infos:
            order_item.order = random.choice(order_list)
            order_item.create_time = order_item.order.create_time
            # 可以考虑同一家店铺商品
        return self._order_item_infos

    def create(self, order_item_info, result_mapping):
        order_item = OrderItem.create(**order_item_info)
        return order_item
        # 以下代码可以考虑添加唯一标示
        # order_item_qs = OrderItem.query().filter()
        # if False and order_item_qs.count():
        #     order_item = order_item_qs[0]
        # else:
        #     order_item = OrderItem.create(**order_item_info)
        # return order_item

    def repair(self, order_item, result_mapping):
        order = order_item.order
        order.status = StatusTypes.PAYED
        total_price = order_item.quantity * order_item.price
        order.total_price += total_price
        order.total_quantity += order_item.quantity
        order.save()
        return order_item

    def delete(self):
        return None


class LogisticsGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        order_list = result_mapping.get(OrderGenerator.get_key())

        logistics_list = []
        # 暂时一笔订单只发一个
        for order in order_list:
            logistics = DictWrapper({})
            logistics.order = order
            logistics.customer = order.customer
            logistics.company = LogisticsCompanyHelper().generate()
            logistics.number = LogisticsNumberHelper().generate()
            logistics.total_quantity = order.total_quantity
            logistics.create_time = order.create_time + datetime.timedelta(days=2)
            logistics_list.append(logistics)
        return logistics_list

    def create(self, logistics_info, result_mapping):
        logistics_qs = Logistics.query().filter(order = logistics_info.order)
        if logistics_qs.count():
            logistics = logistics_qs[0]
        else:
            logistics = Logistics.create(**logistics_info)
        return logistics

    def repair(self, logistics, result_mapping):
        return logistics

    def delete(self):
        return None


class LogisticsItemGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        logistics_list = result_mapping.get(LogisticsGenerator.get_key())

        item_list = []
        # 暂时一笔订单只发一个
        for logistics in logistics_list:
            for order_item in OrderItem.query(order = logistics.order):
                item = DictWrapper({})
                item.logistics = logistics
                item.customer = logistics.customer
                item.order_item = order_item
                item.quantity = order_item.quantity
                item_list.append(item)
        return item_list

    def create(self, item_info, result_mapping):
        item_qs = LogisticsItem.query().filter(order_item = item_info.order_item)
        if item_qs.count():
            item = item_qs[0]
        else:
            item = LogisticsItem.create(**item_info)
        return item

    def repair(self, item, result_mapping):
        order = item.logistics.order
        order.status = StatusTypes.SENDED
        order.save()
        return item

    def delete(self):
        return None


class ServiceGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        order_list = result_mapping.get(OrderGenerator.get_key())

        service_list = []
        for order in order_list:
            service = DictWrapper({})
            server = StaffHelper().generate()
            service.customer = order.customer
            service.order = order
            service.seller = order._chance.staff
            service.server = server
            service.end_time = order.create_time + datetime.timedelta(days = 365)
            service.remark = "服务单备注"
            service_list.append(service)
        return service_list

    def create(self, service_info, result_mapping):
        service_qs = Service.query().filter(order = service_info.order)
        if service_qs.count():
            service = service_qs[0]
        else:
            service = Service.create(**service_info)
        return service

    def repair(self, service, result_mapping):
        order = service.order
        order.status = StatusTypes.FINISHED
        order.save()
        return service

    def delete(self):
        return None


class ServiceItemGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        item_list = result_mapping.get(LogisticsItemGenerator.get_key())
        service_list = result_mapping.get(ServiceGenerator.get_key())
        service_mapping = {service.order : service for service in service_list}

        service_item_list = []
        for item in item_list:
            try:
                product_model = item.order_item.goods.product_model
                order = item.order_item.order
            except Exception as e:
                # 当获取不到信息时，默认跳过发货(理论上应该是发货前，发货中，发货后）
                continue

            for _ in range(item.quantity):
                try:
                    equipment = EquipmentModelHelper().generate(\
                        product_model = product_model, can_send = True)
                    service_item = DictWrapper({})
                    service_item.customer = item.customer
                    service_item.order = order
                    service_item.service = service_mapping.get(order)
                    service_item.equipment = equipment
                    service_item.buyinfo_status = EquipStatusHelper().generate()
                    service_item.dsinfo_status = EquipStatusHelper().generate()
                    service_item.rebate_status = EquipStatusHelper().generate()
                    service_item.sn_status = EquipStatusHelper().generate()
                    service_item.remark = "设备服务单备注"
                    service_item_list.append(service_item)
                except Exception as e:
                    print("缺少库存")

        return service_item_list

    def create(self, service_item_info, result_mapping):
        service_item_qs = ServiceItem.query().filter(
            service = service_item_info.service,
            equipment = service_item_info.equipment
        )
        if service_item_qs.count():
            service_item = service_item_qs[0]
        else:
            service_item = ServiceItem.create(**service_item_info)
        return service_item

    def repair(self, service_item, result_mapping):
        return service_item

    def delete(self):
        return None
