# coding=UTF-8

import json

from model.store.model_order import Order
from model.store.model_service import Service, ServiceItem

class ServiceRepair():


    def run(self):
        self.ready()

        i = 0
        order_qs = Order.search()
        print("==========订单数：", len(order_qs))

        for order in order_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>处理:", i)

            service_list = self._all_service.get(order, None)
            n = 0
            service_only = None
            if service_list is not None and  len(service_list) > 1:
                for service in service_list:
                    n = n + 1;
                    if n == 1:
                        service_only = service
                    else:
                        ServiceItem.search(service = service).update(service = service_only)
                        service.delete()


    def ready(self):
        self._all_service = {}

        service_qs = Service.query()
        print("=====服务单数据数=====", len(service_qs))
        for service in service_qs:
            if service.order not in self._all_service:
                self._all_service[service.order] = [service]
            else:
                self._all_service[service.order].append(service)

        print("=====数据准备完成=====")

