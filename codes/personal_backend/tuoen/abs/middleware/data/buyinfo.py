# coding=UTF-8
import re
import datetime
import json
from tuoen.sys.utils.common.timetools import add_month

from django.db.models import *

from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField, ExcelDeletePointField
from model.store.model_import import ImportCustomerBuyinfo, ImportStatus
from tuoen.abs.middleware.department import department_middleware


from model.store.model_user import Staff
from model.store.model_staff_alias import StaffAlias
from model.store.model_mobilephone import MobileDevices, MobileMaintain
from model.store.model_shop import Shop, Goods
from model.store.model_customer import Customer
from model.store.model_order import Order, StatusTypes, OrderItem
from model.store.model_customer_chance import SaleChance
from model.store.model_order_event import StaffOrderEvent, IsCount
from model.store.model_logistics import Logistics, LogisticsItem
from model.store.model_equipment import Equipment, EquipmentStatusState
from model.store.model_equipment_sn import EquipmentSn, SnStatusType
from model.store.model_equipment_register import EquipmentRegister, RegisterTypes
from model.store.model_equipment_rebate import EquipmentRebate
from model.store.model_equipment_transaction import EquipmentTransaction
from model.store.model_service import Service, ServiceItem
from model.store.model_equipment_in import EquipmentIn
from model.store.model_equipment_out import EquipmentOut, AgentTypes
from model.store.model_product import ProductModel
from model.store.model_measure_staff import MeasureStaff
from model.store.model_auth_access import AuthAccess, AccessTypes
from model.store.model_repenishment import ReplenishmentItem, Restatus
from model.store.model_merchant_equipment import MerchantEquipment


from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.abs.middleware.journal import JournalMiddleware

class BuyinfoImport(ExcelImport):

    def __init__(self):
        self._staff = None
        self._server_staff = None
        self._mobiledevices = None
        self._shop = None
        self._equipment_in = None
        self._product_model = None
        self._device_code = ""
        self._error_msg = ""
        self._remark_pure = ""
        self._is_new_order = True
        self._is_new_logistics = True
        self._equipment = None
        self._equipment_sn = None
        self._equipment_register = None
        self._department = None
        self._is_reissue = False
        self._replenishment_code = ""
        self._replenishment_item = None
        self._order_sn = ""
        self._is_ysb = False

    def get_exec_cls(self):
        return ImportCustomerBuyinfo

    def get_redis_name(self):
        return "ImportCustomerBuyinfo"

    def get_fields(self):
        check_list = [
            ['serial_number', IntField(desc = "序号")],
            ['order_sn', CharField(desc = "订单编号")],
            ['goods_sn', CharField(desc = "商品编号")],
            ['buy_number', IntField(desc = "购买数量")],
            ['buy_money', ExcelMoneyField(desc = "订单金额/分")],
            ['pay_time', ExcelDateTimeField(desc = "付款时间")],
            ['shop_name', CharField(desc = "网点名称")],
            ['buy_name', CharField(desc = "买家姓名")],
            ['province', CharField(desc = "省")],
            ['city', CharField(desc = "市")],
            ['area', CharField(desc = "区")],
            ['address', CharField(desc = "详细地址")],
            ['logistics_company', CharField(desc = "物流公司")],
            ['logistics_code', CharField(desc = "物流单号")],
            ['buy_phone', ExcelDeletePointField(desc = "联系方式")],
            ['remark', CharField(desc = "客服备注")],
            ['buy_nick', CharField(desc = "卖家账号")],
            ['device_code', CharField(desc = "设备编码")],
        ]
        return check_list

    def exec_convet(self, buyinfo):

        check_integrity = self.check_data_integrity(buyinfo)

        if not check_integrity:
            return False, self._error_msg

        customer = self.convet_customer(buyinfo.buy_name, buyinfo.province, buyinfo.city, \
                                        buyinfo.area, buyinfo.address, buyinfo.buy_phone, \
                                        buyinfo.buy_nick)

        goods = self.convet_goods(buyinfo.goods_sn, buyinfo.buy_number, buyinfo.buy_money)

        order = self.convet_order(self._order_sn, goods.price, 1, \
                                  buyinfo.pay_time, buyinfo.buy_name, buyinfo.province, buyinfo.city, \
                                  buyinfo.area, buyinfo.address, buyinfo.buy_phone, customer)


        order_item = self.convet_order_item(order, goods)

        if self._is_new_order:
            sale_chance = self.convet_sale_chance(self._staff, customer, goods, order)
            # 新人保护期订单事件打标识
            is_count = IsCount.COUNTIN
            if self._staff.p_end_time is not None:
                if order.pay_time < self._staff.p_end_time:
                    is_count = IsCount.COUNTOUT
            staff_order_event = StaffOrderEvent.create(staff = self._staff, order = order, remark = self._remark_pure, \
                                                       department = self._department, is_count = is_count)

        logistics = self.convet_logistics(order, customer, buyinfo.logistics_company, buyinfo.logistics_code)


        logistics_item = self.convet_logistics_item(logistics, order_item, customer)


        if self._is_new_order:
            service = Service.create(seller = self._staff, server = self._staff,
                                     customer = customer, order = order, \
                                     end_time = datetime.datetime.now() + datetime.timedelta(days = 5))
        else:
            service = Service.query(order = order)[0]

        if self._equipment is None:
            self._equipment = Equipment.create(customer = customer, logistics_item = logistics_item, order = order, \
                                         code = self._device_code, product_model = self._product_model, product = self._product_model.product)

            equipment_sn = EquipmentSn.create(customer = customer, order = order, equipment = self._equipment, \
                                         code = self._device_code, product_model = self._product_model, product = self._product_model.product)

            dsinfo_status = SnStatusType.RED
            rebate_status = SnStatusType.RED
            service_item = ServiceItem.create(customer = customer, service = service, \
                                      equipment_sn = equipment_sn, order = order, \
                                      sn_status = SnStatusType.GREEN, \
                                      dsinfo_status = dsinfo_status, rebate_status = rebate_status)
            if not self._is_ysb:
                # 商品为点刷
                equipment_register_qs = EquipmentRegister.search(device_code = self._device_code)


                if equipment_register_qs.count() > 0:
                    dsinfo_status = SnStatusType.YELLOW
                    self._equipment_register = equipment_register_qs[0]
                    self._equipment_register.update(equipment_sn = equipment_sn, status = RegisterTypes.NORMAL)
                    rebate_status = self.calculation_rebate_status()
                    service_item.update(dsinfo_status = dsinfo_status, rebate_status = rebate_status)
            else:
                # 商品为银收宝(暂无计算激活率)
                merchant_equipment_qs = MerchantEquipment.query(serial_no = self._device_code)
                if merchant_equipment_qs.count() > 0:
                    merchant_equipment = merchant_equipment_qs[0]
                    dsinfo_status = SnStatusType.YELLOW
                    merchant_equipment.update(equipment_sn = equipment_sn)
                    service_item.update(dsinfo_status = dsinfo_status, rebate_status = rebate_status)
        else:
            # 迁移数据sn绑定，则为售后机,否则迁移数据
            if self._equipment_sn.order:
                self._equipment.update(customer = customer, logistics_item = logistics_item, order = order)
            else:
                service_item_qs = ServiceItem.search(equipment_sn = self._equipment_sn)
                self._equipment.update(customer = customer, logistics_item = logistics_item, order = order)
                self._equipment_sn.update(customer = customer, order = order)
                if service_item_qs.count() > 0:
                    service_item_qs[0].update(customer = customer, service = service, order = order)

        # 更新物流详情sn冗余信息
        self.update_logistice_item(logistics_item, self._equipment)

        # 生成绩效
        if self._staff is not None:
            self.convet_measure_staff(self._staff, order.pay_time)

        # 判断是否为补货
        if self._is_reissue and self._replenishment_code:
            self._replenishment_item.update(status = Restatus.DONE)
            Equipment.search(code = self._replenishment_code).update(equipment_status = EquipmentStatusState.PATCH)
            EquipmentSn.search(code = self._replenishment_code).update(sn_status = EquipmentStatusState.PATCH)

        return True, ""


    def general_measure_staff(self):

        pass

    def check_data_integrity(self, buyinfo):
        if not buyinfo.device_code:
            self._error_msg = "缺少设备编码"
            return False
        if not buyinfo.order_sn:
            self._error_msg = "缺少订单编号"
            return False

        self._order_sn = self.analysis_order_sn(buyinfo.order_sn)

        if  len(self._order_sn) > 120:
            self._error_msg = "订单编号太长"
            return False
        if not buyinfo.shop_name:
            self._error_msg = "缺少店铺名称"
            return False
        if not buyinfo.buy_name:
            self._error_msg = "缺少购买人姓名"
            return False
        if not buyinfo.buy_phone:
            self._error_msg = "缺少购买人联系方式"
            return False
        if self.contain_zh(buyinfo.buy_phone.strip()):
            self._error_msg = "购买电话存在汉字"
            return False
        if not buyinfo.goods_sn:
            self._error_msg = "缺少商品编号"
            return False
        if not buyinfo.remark:
            self._error_msg = "缺少备注信息"
            return False
        if "售后" in buyinfo.remark:
            self._error_msg = "售后机无法导入"
            return False

        check_repeat = self.skip_repeat(buyinfo.device_code)
        if not check_repeat:
            return False

        check_remark = self.analysis_remark(buyinfo.remark)
        if not check_remark:
            return False

        if buyinfo.shop_name in self._shop_mapping:
            shop = self._shop_mapping[buyinfo.shop_name]
        else:
            shop = Shop.get_shop_buyname(buyinfo.shop_name)
            if shop is None:
                self._error_msg = "该店铺系统不存在，请通知相关人员进行添加"
                return False

        # --- bug
        self._shop = shop
        return True

    def handle_device_code(self, device_code):
        self._is_ysb = False
        device_code = device_code.strip()
        device_code_len = len(device_code)
        if device_code_len == 19:
            device_code = device_code[4:]
        elif device_code_len == 20:
            device_code = device_code[4:-1]
        elif device_code_len == 10:
            self._is_ysb = True
        else:
            self._error_msg = "该设备编码位数异常"
            return False, 0

        return True, device_code

    def contain_zh(self, word):
        '''判断传入字符串是否包含中文:param word: 待判断字符串:return: True:包含中文  False:不包含中文'''

        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = zh_pattern.search(word)
        if match:
            return True
        else:
            return False

    def skip_repeat(self, code):
        code_check, device_code = self.handle_device_code(code)
        if not code_check:
            return False

        # --- performace
        self._equipment = None
        equipment_qs = Equipment.search(code = device_code)
        if equipment_qs.count() > 0:
            equipment = equipment_qs[0]
            if equipment.order:
                self._error_msg = "该设备编码重复"
                return False
            else:
                self._equipment = equipment
                self._equipment_sn = EquipmentSn.search(equipment = equipment)[0]
        else:
            if not self._is_ysb:
                equipment_in_qs = EquipmentIn.search(min_number__lte = device_code, \
                                                     max_number__gte = device_code)
                if equipment_in_qs.count() > 0:
                    self._equipment_in = equipment_in_qs[0]
                    product_model_qs = ProductModel.query().filter(name = self._equipment_in.product_model)
                    if product_model_qs.count() > 0:
                        self._product_model = product_model_qs[0]
                    else:
                        self._error_msg = "该设备型号不存在，请联系管理员添加"
                        return False
                else:
                    self._error_msg = "该设备编码号段异常，不在入库号段内"
                    return False

                equipment_out_qs = EquipmentOut.search(min_number__lte = device_code, \
                                                     max_number__gte = device_code, type = AgentTypes.SELF)
                if equipment_out_qs.count() == 0:
                    self._error_msg = "该设备编码号段异常，不在出库号段内"
                    return False
            else:
                product_model_qs = ProductModel.query().filter(name = "P27")
                if product_model_qs.count() > 0:
                    self._product_model = product_model_qs[0]
                else:
                    self._error_msg = "该设备型号不存在，请联系管理员添加"
                    return False
                pass

        self._device_code = device_code

        return True

    def analysis_remark(self, remark):
            try:
                staff_name = re.findall(".*kf(.*)kf.*", remark)[0].strip()
                check_staff = self.convet_staff(staff_name)
                if not check_staff:
                    return False
                else:
                    auth_access_qs = AuthAccess.search(staff = self._staff, access_type = AccessTypes.DEPARTMENT)
                    if auth_access_qs.count() > 0:
                        self._department = department_middleware.get_self(auth_access_qs[0].access_id)
                    else:
                        self._error_msg = "该备注客服没有部门"
                        return False
            except Exception as e:
                self._error_msg = "缺少备注客服"
                return False
            try:
                mobile_code = re.findall(".*wx(.*)wx.*", remark)[0].strip()
                check__mobiledevices = self.convet_mobiledevices(mobile_code)
                if not check__mobiledevices:
                    return False
            except Exception as e:
                self._error_msg = "缺少备注手机编码"
                return False
            try:
                self._remark_pure = re.findall(".*bz(.*)bz.*", remark)[0].strip()
            except Exception as e:
                self._remark_pure = ""
                pass

            try:
                self._replenishment_code = re.findall(".*bf(.*)bf.*", remark)[0].strip()
            except Exception as e:
                self._replenishment_code = ""
                pass

            return True

    def convert_prepare(self, convert_list):
        goods_sn_set = set()
        shop_name_set = set()
        for obj in convert_list:
            goods_sn_set.add(obj.goods_sn)
            shop_name_set.add(obj.shop_name)

        goods_sn_list = list(goods_sn_set)
        shop_name_list = list(shop_name_set)
        self._goods_mapping = { goods.name : goods for goods in \
                         Goods.query().filter(name__in = goods_sn_list)}

        self._shop_mapping = { shop.name : shop for shop in \
                              Shop.query().filter(name__in = shop_name_list)}

        return convert_list, []

    def convet_staff(self, staff_name):
        staff_number_qs = Staff.search(number = staff_name)
        if staff_number_qs.count() > 0:
             self._staff = staff_number_qs[0]
        else:
            staff_alias_qs = StaffAlias.search(alias = staff_name)
            if staff_alias_qs.count() > 0:
                self._staff = staff_alias_qs[0].staff
            else:
                staff_name = self.format_str(staff_name)
                staff_qs = Staff.search(name = staff_name)
                if staff_qs.count() > 0:
                    self._staff = staff_qs[0]
                else:
                    self._error_msg = "备注客服不存在"
                    return False

        return True

    def is_chinese(self, uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False


    def format_str(self, content):
        content_str = ''
        for i in content:
            if self.is_chinese(i):
                content_str = content_str + i
        return content_str


    def convet_mobiledevices(self, mobile_code):
        # --- performace
        mobile_devices_qs = MobileDevices.query().filter(code = mobile_code)
        if mobile_devices_qs.count() > 0:
            self._mobiledevices = mobile_devices_qs[0]
            mobile_maintain_qs = MobileMaintain.search(devices = self._mobiledevices)
            if mobile_maintain_qs.count() > 0:
                self._server_staff = mobile_maintain_qs[0].staff
        else:
            self._error_msg = "备注手机编码系统不存在"
            return False

        return True

    def convet_customer(self, name, province, city, area, address, buy_phone, buy_nick):
        customer = None
        phone = buy_phone.strip()[:11]
        # --- performace
        customer_qs = Customer.search(phone = phone)
        if customer_qs.count() > 0:
            customer = customer_qs[0]
            # 没有手机编码则更新
            customer.update(mobiledevices = self._mobiledevices)
        else:
            city_info = "{p}{c}{a}".format(p = province, c = city, a = area)
            customer = Customer.create(name = name, city = city_info, address = address, phone = phone, \
                                       nick = buy_nick, mobiledevices = self._mobiledevices, remark = buy_phone)
        return customer

    def convet_goods(self, name, buy_number, buy_money):
        goods = None
        try:
            price = int(buy_money / buy_number)
        except Exception as e:
            price = 0

        if name in self._goods_mapping:
            goods = self._goods_mapping[name]
            if goods.price != price:
                goods.update(price = price)
        else:
            goods_qs = Goods.query().filter(name = name)
            if goods_qs.count() > 0:
                goods = goods_qs[0]
                if goods.price != price:
                    goods.update(price = price)
            else:
                goods = Goods.create(name = name, alias = name, price = price, shop = self._shop, product_model = self._product_model)

        return goods

    def convet_order(self, order_sn, buy_money, buy_number, pay_time, buy_name, province, city, \
                     area, address, buy_phone, customer):
        order = None
        # -- performace
        order_qs = Order.search(order_sn = order_sn)
        if order_qs.count() > 0:
            self._is_new_order = False
            order = order_qs[0]
            if not self._is_reissue:
                order.update(total_price = order.total_price + buy_money, total_quantity = order.total_quantity + 1)
        else:
            self._is_new_order = True
            city_info = "{p}{c}{a}".format(p = province, c = city, a = area)
            order = Order.create(order_sn = order_sn, total_price = buy_money, total_quantity = buy_number, \
                                 pay_time = pay_time, status = StatusTypes.SENDED, consignee = buy_name, \
                                 city = city_info, address = address, phone = buy_phone, customer = customer, \
                                 shop = self._shop, remark = self._remark_pure)
        return order

    def convet_order_item(self, order, goods):
        order_item = None
        order_item_qs = OrderItem.search(order = order, goods = goods)
        if order_item_qs.count() > 0:
            order_item = order_item_qs[0]
            if not self._is_reissue:
                order_item.update(quantity = order_item.quantity + 1)
        else:
            order_item = OrderItem.create(order = order, goods = goods, name = goods.name, alias = goods.name, \
                                          code = goods.code, price = goods.price, rate = goods.code, introduction = goods.introduction, \
                                          thumbnail = goods.thumbnail, postage = goods.postage, quantity = 1)
        return order_item


    def convet_logistics(self, order, customer, logistics_company, logistics_code):
        logistics = None
        logistics_qs = Logistics.query(order = order, number = logistics_code)
        if logistics_qs.count() > 0:
            logistics = logistics_qs[0]
            logistics.update(total_quantity = logistics.total_quantity + 1)
        else:
            logistics = Logistics.create(order = order, customer = customer, company = logistics_company, \
                                         number = logistics_code, total_quantity = 1)

        return logistics

    def convet_logistics_item(self, logistics, order_item, customer):
        logistics_item = None
        logistics_item_qs = LogisticsItem.query(logistics = logistics, order_item = order_item)
        if logistics_item_qs.count() > 0:
            logistics_item = logistics_item_qs[0]
            logistics_item.update(quantity = logistics_item.quantity + 1)
        else:
            logistics_item = LogisticsItem.create(customer = customer, logistics = logistics, order_item = order_item, \
                                                  quantity = 1)

        return logistics_item

    def update_logistice_item(self, logistics_item, equipment):
        equipment_sns = json.loads(logistics_item.equipment_sn_list)
        equipment_sns.append(equipment.code)
        equipment_sn_list = json.dumps(equipment_sns)
        logistics_item.update(equipment_sn_list = equipment_sn_list)

    def convet_sale_chance(self, staff, customer, goods, order):
        sale_chance = None
        sale_chance_qs = SaleChance.search(create_time__lt = order.pay_time, end_time__gte = order.pay_time, \
                                           customer = customer, staff = staff, shop = self._shop, goods = goods)
        if sale_chance_qs.count() > 0:
            sale_chance = sale_chance_qs[0]
            order_list = json.loads(sale_chance.order_ids)
            order_list.append(order.id)
            order_ids = json.dumps(order_list)
            sale_chance.update(order_count = sale_chance.order_count + 1, order_ids = order_ids)
        else:
            create_time = order.pay_time - datetime.timedelta(days = 10)
            end_time = order.pay_time + datetime.timedelta(days = 5)
            sale_chance = SaleChance.create(staff = staff, customer = customer, shop = self._shop, goods = goods, \
                                            order_count = 1, order_ids = [order.id], end_time = end_time, \
                                             create_time = create_time)
        return sale_chance

    def convet_measure_staff(self, staff, pay_time):
        buy_data = datetime.datetime(pay_time.year, pay_time.month, pay_time.day)
        # --- performace
        measure_staff_qs = MeasureStaff.search(staff = staff, report_date = buy_data)
        if measure_staff_qs.count() == 0:
            MeasureStaff.create(staff = staff, report_date = buy_data, department = self._department)


    def remove(self, buyinfo_id):
        icb_qs = ImportCustomerBuyinfo.search(id__in = buyinfo_id)
        if icb_qs.count() > 0:
            icb_qs.delete()
        else:
            raise BusinessError("條目不存在")

    def reset_status(self, **search_info):
        search_info.update({'status__in': [ImportStatus.EXCUTTING, ImportStatus.FAILED]})
        if "create_time_start" in search_info:
            search_info.update({'create_time__gte': search_info.pop("create_time_start")})
        if "create_time_end" in search_info:
            search_info.update({'create_time__lt': search_info.pop("create_time_end")})
        try:
            ImportCustomerBuyinfo.search(**search_info).update(status = ImportStatus.INIT, error_text = '')
        except Exception as e:
            raise  BusinessError("恢復初始化失敗")

    def calculation_rebate_status(self):
        rebate_status = SnStatusType.RED
        rebate_money = self._equipment.product.rebate_money
        if rebate_money > 0:
            last_time = add_month(self._equipment_register.bind_time, 2)
            total_money_lastmonth = EquipmentTransaction.sum_money(transaction_time__range = (self._equipment_register.bind_time, last_time), \
                                                                   code = self._equipment_register)
            if total_money_lastmonth >= rebate_money:
               equipment_rebate_qs = EquipmentRebate.query().filter(code = self._equipment_register, remark__contains = "已达到")
               if equipment_rebate_qs.count() > 0:
                   rebate_status = SnStatusType.TGREEB
               else:
                   rebate_status = SnStatusType.GREEN
            else:
                total_money = EquipmentTransaction.sum_money(code = self._equipment_register)
                if total_money >= rebate_money:
                    rebate_status = SnStatusType.YELLOW

        return rebate_status

    def analysis_order_sn(self, order_sn):
        if "_BF" in order_sn:
            self._is_reissue = True
            split_list = order_sn.split("_BF")
            order_sn = split_list[0]
            replenishment_item_id = split_list[1]
            self._replenishment_item = ReplenishmentItem.get_byid(int(replenishment_item_id))
        else:
            self._is_reissue = False
            self._replenishment_item = None
        return order_sn

