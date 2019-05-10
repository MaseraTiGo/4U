# coding=UTF-8
import json
import datetime
import time
import re
from multiprocessing import Pool
import threading

from support.transfer.base import BaseTransfer
from model.store.model_customer import Customer
from model.store.model_equipment import Equipment
from model.store.model_mobilephone import MobileDevices, MobileMaintain
from model.store.model_shop import Shop, Goods
from model.store.model_product import ProductModel
from model.store.model_order import Order, OrderItem
from model.store.model_customer_chance import SaleChance
from model.store.model_order_event import StaffOrderEvent
from model.store.model_logistics import Logistics, LogisticsItem
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_service import Service, ServiceItem
from model.store.model_record_error import RecordError
from model.store.model_import import ImportCustomerBuyinfo
from model.store.model_equipment_in import EquipmentIn
from model.store.model_equipment_out import EquipmentOut
from model.store.model_measure_staff import MeasureStaff


class EquipmentTransfer(BaseTransfer):

    def __init__(self):
        self._error_text = ""
        self._product_model = None
        self._sys_shop = Shop.get_shop_buyname("系统店铺")
        self._sys_goods = Goods.query().filter(name = "系统商品")[0]
        self._sys_customer = Customer.search(name = "系统客户")[0]


    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select a.create_date,a.modify_date,a.nickname,a.buy_address,a.buy_date,a.buy_mobile,\
            a.customer_name,a.product_name,a.terminal_code,a.wechat,a.wechatname,a.wechat_index,a.shopname,\
            a.remarks,a.document_number,a.buy_num,a.buy_name,a.wl_number,a.wl_company,a.sn_color,\
            a.order_id,a.buy_price,a.buyinfo_color,b.name as staff_name,c.name as shop_name from ct_channel_user a \
            left join ct_admin b ON a.customer=b.id left join ct_sale_channel c ON a.sale_channel_id=c.id where \
            a.is_buyinfo=1 and a.terminal_code in ('850300010768677','850300010766727','850300010772191')"

    def get_total(self):
        sql = "select count(*) as total from ct_channel_user a \
            left join ct_admin b ON a.customer=b.id left join ct_sale_channel c ON a.sale_channel_id=c.id where \
            a.is_buyinfo=1"
        self.check_conn()
        self._cursor.execute(sql)
        result = self._cursor.fetchall()[0]
        return result['total']

    def run(self):
        self.base_sql()
        """
        limit = 1000
        thread_num = 10

        total = self.get_total()
        db_times = int(total / limit)
        db_times = db_times + 1 if total % limit else db_times

        is_rest = db_times % thread_num
        cycle = int(db_times / thread_num)
        cycle = cycle + 1 if is_rest else cycle

        count = 0
        for cycle_index in range(cycle):
            thread_list = []
            for index in range(thread_num):
                times = cycle_index * thread_num + index
                if times > db_times:
                    break

                sql = self.generate_sql(times, limit)
                print("============> ", sql)
                data_list = self.get_date_list(sql)
                cur_thread = threading.Thread(target = self.generate_date, args = (data_list,))
                # cur_thread.setDaemon(True)
                thread_list.append(cur_thread)
                count += len(data_list)

            for thread in thread_list:
                thread.start()

            for thread in thread_list:
                thread.join()

            print("finish to deal data for items :  count --> ", count)

        """

        current = 0
        count = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        while len(data_list) > 0:
            count += len(data_list)
            print("start to deal data for items :  count --> ", count)
            self.generate_date(data_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)


        self.break_link()
        print("==================成功结束==================")


    def convert_data(self, dic_data):
        self._modify_date = dic_data["modify_date"]
        self._create_date = dic_data["create_date"]

        # 获取员工
        staff = self.get_staff_byname(dic_data["staff_name"])

        # 获取手机设备
        mobile_devices = self.get_mobile_devices(dic_data["wechat_index"])

        # 获取店铺
        shop = self.get_shop(dic_data["shop_name"], dic_data["shopname"], dic_data["terminal_code"])

        # 获取客户
        customer = self.get_customer(dic_data["nickname"], dic_data["buy_address"], \
                                     dic_data["buy_mobile"], dic_data["buy_name"], \
                                     mobile_devices, dic_data["terminal_code"])

        # 获取商品
        goods = self.get_goods(dic_data["product_name"], dic_data["buy_num"], \
                               dic_data["buy_price"], shop, dic_data["terminal_code"])

        # 获取订单
        order = self.get_order(dic_data["buy_address"], dic_data["buy_date"], dic_data["buy_mobile"], \
                               dic_data["remarks"], dic_data["buy_num"], dic_data["buy_name"], \
                               dic_data["order_id"], dic_data["buy_price"], customer, shop, dic_data["document_number"], \
                               dic_data["terminal_code"])

        # 获取订单详情
        order_item = OrderItem.create(order = order, goods = goods, name = goods.name, \
                                  alias = goods.name, price = goods.price, \
                                  quantity = order.total_quantity, update_time = dic_data["modify_date"], \
                                  create_time = dic_data["create_date"])

        # 获取销售机会
        sale_chance = self.get_sale_chance(staff, customer, shop, goods, order.pay_time, order)

        # 获取订单事件
        if staff is not None:
            staff_order_event = StaffOrderEvent.create(staff = staff, order = order, remark = dic_data["remarks"], \
                                                       update_time = dic_data["modify_date"], create_time = dic_data["create_date"])

        # 获取物流
        company = dic_data["wl_company"] if dic_data["wl_company"] else "顺丰速运"
        number = dic_data["wl_number"] if dic_data["wl_number"] else "BQ001"
        logistics = Logistics.create(order = order, customer = customer, company = company, \
                                     number = number, total_quantity = order.total_quantity, \
                                     update_time = dic_data["modify_date"], create_time = dic_data["create_date"])

        # 获取物流详情
        logistics_item = LogisticsItem.create(customer = customer, logistics = logistics, order_item = order_item, \
                                              quantity = order.total_quantity, \
                                              update_time = dic_data["modify_date"], \
                                              create_time = dic_data["create_date"])

        product = self._product_model.product if self._product_model else None
        equipment = self.skip_equipment(dic_data["terminal_code"])

        # 获取售后服务人
        server_staff = None
        if mobile_devices is not None:
            server_staff = self.get_server_staff(mobile_devices)

        # 获取售后服务单
        service = Service.create(seller = staff, server = server_staff, customer = customer, order = order, \
                                 end_time = order.pay_time + datetime.timedelta(days = 365), \
                                 update_time = dic_data["modify_date"], create_time = dic_data["create_date"])

        # 生成绩效
        if staff is not None:
            self.convet_measure_staff(staff, order.pay_time)

        # 判断是否存在该设备
        if equipment is None:
            # 获取设备信息
            equipment = Equipment.create(customer = customer, logistics_item = logistics_item, order = order, \
                                         code = dic_data["terminal_code"], product_model = self._product_model, \
                                         product = product, update_time = dic_data["modify_date"], \
                                         create_time = dic_data["create_date"])

            # 获取售后服务单详情
            service_item = ServiceItem.create(customer = customer, service = service, equipment = equipment, \
                                              order = order, buyinfo_status = dic_data["buyinfo_color"], \
                                              dsinfo_status = "red", \
                                              sn_status = dic_data["sn_color"], \
                                              rebate_status = "red", \
                                              update_time = dic_data["modify_date"], \
                                              create_time = dic_data["create_date"])
        else:
            # 获取售后服务单详情
            service_item_qs = ServiceItem.search(equipment = equipment)
            service_item = service_item_qs[0]

            # 获取设备信息
            equipment.update(customer = customer, logistics_item = logistics_item, order = order, \
                                         product_model = self._product_model, \
                                         product = product)

            service_item.update(customer = customer, service = service, \
                               order = order, buyinfo_status = dic_data["buyinfo_color"])

        return True


    def skip_data(self, code):
        equipment = None
        if code:
            equipment_qs = Equipment.search(code = code, order__isnull = False)
            if equipment_qs.count() > 0:
                return False

        return True


    def generate_date(self, data_list):
        for dic_data in data_list:
            if not self.check_data(dic_data):
                continue

            try:
                self.convert_data(dic_data)
            except Exception as e:
                error_info = "data: {} , error = {}".format(dic_data, e)
                RecordError.create(remark = error_info)

    def check_data(self, dic_data):

        if not dic_data["order_id"] and not dic_data["document_number"]:
            self._error_text = "订单id和单据编号都为空"
            self.save_error_data(dic_data)
            return False

        if not dic_data["buy_date"]:
            self._error_text = "购买时间为空"
            self.save_error_data(dic_data)
            return False

        if not dic_data["terminal_code"]:
            self._error_text = "设备编码为空"
            self.save_error_data(dic_data)
            return False
        else:
            if not self.is_number(dic_data["terminal_code"]):
                self._error_text = "设备编码不为纯数字"
                self.save_error_data(dic_data)
                return False
            if not self.skip_data(dic_data["terminal_code"]):
                self._error_text = "重复数据"
                print("===================", self._error_text)
                return False

        if len(dic_data["terminal_code"]) != 15:
            self._error_text = "设备编码长度不为15位"
            self.save_error_data(dic_data)
            return False

        if self.contain_zh(dic_data["buy_mobile"].strip()):
            self._error_text = "购买电话存在汉字"
            self.save_error_data(dic_data)
            return False

        if not self.check_quipment_in_and_out(dic_data["terminal_code"]):
            self.save_error_data(dic_data)
            return False

        return True

    def save_error_data(self, dic_data):
        try:
            ImportCustomerBuyinfo.create(order_sn = dic_data["order_id"] if dic_data["order_id"] else dic_data["document_number"], \
                                         goods_sn = dic_data["product_name"], \
                                         buy_number = dic_data["buy_num"], buy_money = dic_data["buy_price"], pay_time = dic_data["buy_date"], \
                                         shop_name = dic_data["shopname"], buy_name = dic_data["buy_name"], \
                                         address = dic_data["buy_address"], logistics_company = dic_data["wl_company"], \
                                         logistics_code = dic_data["wl_number"], buy_phone = dic_data["buy_mobile"], remark = dic_data["remarks"], \
                                         buy_nick = dic_data["nickname"], device_code = dic_data["terminal_code"], \
                                         status = "failed", error_text = self._error_text)
        except Exception as e:
            error_info = "data: {} , error = {}".format(dic_data, e)
            RecordError.create(remark = error_info)
        return True

    def contain_zh(self, word):
        '''判断传入字符串是否包含中文:param word: 待判断字符串:return: True:包含中文  False:不包含中文'''

        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = zh_pattern.search(word)
        if match:
            return True
        else:
            return False


    def generate_sql(self, current, limit = 1000):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)


    def skip_equipment(self, code):
        equipment = None
        if code:
            equipment_qs = Equipment.search(code = code)
            if equipment_qs.count() > 0:
                equipment = equipment_qs[0]

        return equipment


    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False


    def check_quipment_in_and_out(self, terminal_code):
        equipment_in_qs = EquipmentIn.search(min_number__lte = terminal_code, \
                                             max_number__gte = terminal_code)
        if equipment_in_qs.count() > 0:
            equipment_in = equipment_in_qs[0]
            product_model_qs = ProductModel.query().filter(name = equipment_in.product_model)
            if product_model_qs.count() > 0:
                self._product_model = product_model_qs[0]
            else:
                self._error_text = "该设备型号不存在，请联系管理员添加"
                return False
        else:

            self._error_text = "该设备编码号段异常，不在入库号段内"
            return False
        equipment_out_qs = EquipmentOut.search(min_number__lte = terminal_code, \
                                             max_number__gte = terminal_code)
        if equipment_out_qs.count() == 0:
            self._error_text = "该设备编码号段异常，不在出库号段内"
            return False

        return True

    def get_mobile_devices(self, code):
        mobile_devices = None
        if code:
            mobile_devices_qs = MobileDevices.search(code = code)
            if mobile_devices_qs.count() > 0:
                mobile_devices = mobile_devices_qs[0]
            else:
                mobile_devices = MobileDevices.create(code = code, update_time = self._modify_date, create_time = self._create_date)

        return mobile_devices


    def get_shop(self, shop_name, shopname, terminal_code):
        shop_name = shop_name if shop_name else shopname

        shop = None
        if shop_name:
            shop = Shop.get_shop_buyname(shop_name)
            if shop is None:
                shop = Shop.create(name = shop_name, update_time = self._modify_date, create_time = self._create_date)
        else:
            shop = self._sys_shop
            RecordError.create(remark = "缺少店铺:{c}".format(c = terminal_code))
        return shop


    def get_customer(self, nickname, buy_address, buy_mobile, buy_name, mobile_devices, terminal_code):
        customer = None
        if buy_name and buy_mobile:
            phone = buy_mobile.strip()[:11]
            customer_qs = Customer.search(phone = phone)
            if customer_qs.count() > 0:
                customer = customer_qs[0]
            else:
                customer = Customer.create(name = buy_name, address = buy_address, phone = phone, \
                                           nick = nickname, mobiledevices = mobile_devices, remark = buy_mobile, \
                                           update_time = self._modify_date, create_time = self._create_date)
        else:
            customer = self._sys_customer
            RecordError.create(remark = "缺少客户:{c}".format(c = terminal_code))
        return customer


    def get_goods(self, product_name, buy_num, buy_price, shop, terminal_code):
        goods = None
        if product_name:
            goods_qs = Goods.query().filter(name = product_name)
            if goods_qs.count() > 0:
                goods = goods_qs[0]
            else:
                try:
                    price = int(buy_price * 100 / buy_num)
                except Exception as e:
                    price = 0
                goods = Goods.create(name = product_name, alias = product_name, price = price, \
                                     shop = shop, product_model = self._product_model, \
                                     update_time = self._modify_date, create_time = self._create_date)
        else:
            goods = self._sys_goods
            RecordError.create(remark = "缺少商品:{c}".format(c = terminal_code))

        return goods


    def get_order(self, buy_address, buy_date, buy_mobile, remarks, buy_num, buy_name, order_id, buy_price, \
                  customer, shop, document_number, terminal_code):
        order = None
        order_sn = order_id if order_id else document_number
        order_sn = order_sn[:100]
        order_qs = Order.search(order_sn = order_sn)
        if order_qs.count() > 0:
            order = order_qs[0]
        else:
            try:
                total_price = int(buy_price * 100)
            except Exception as e:
                total_price = 0

            try:
                buy_num = int(buy_num)
            except Exception as e:
                buy_num = 1

            try:
                buy_date = buy_date if buy_date and isinstance(buy_date, datetime.datetime) else self._create_date
            except:
                buy_date = self._create_date

            order = Order.create(order_sn = order_sn, total_price = total_price, total_quantity = buy_num, \
                                 pay_time = buy_date, status = "sended", consignee = buy_name, \
                                 address = buy_address, phone = buy_mobile, customer = customer, \
                                 shop = shop, remark = remarks, update_time = self._modify_date, \
                                 create_time = self._create_date)

        return order


    def get_sale_chance(self, staff, customer, shop, goods, buy_date, order):
        sale_chance = None
        sale_chance_qs = SaleChance.search(create_time__lt = buy_date, end_time__gte = buy_date, \
                                           customer = customer, shop = shop, goods = goods)
        if sale_chance_qs.count() > 0:
            sale_chance = sale_chance_qs[0]
            try:
                order_list = json.loads(sale_chance.order_ids)
            except:
                order_list = []
            order_list.append(order.id)
            order_count = len(order_list)
            order_ids = json.dumps(order_list)
            sale_chance.update(order_count = order_count, order_ids = order_ids)
        else:
            create_time = buy_date - datetime.timedelta(days = 10)
            end_time = buy_date + datetime.timedelta(days = 5)
            order_list = [order.id]
            order_count = len(order_list)
            order_ids = json.dumps(order_list)
            sale_chance = SaleChance.create(staff = staff, customer = customer, shop = shop, goods = goods, \
                                            order_count = order_count, order_ids = order_ids, end_time = end_time, \
                                             create_time = create_time)
        return sale_chance

    def get_server_staff(self, mobile_devices):
        server_staff = None
        mobile_maintain_qs = MobileMaintain.search(devices = mobile_devices)
        if mobile_maintain_qs.count() > 0:
            server_staff = mobile_maintain_qs[0].staff
        return server_staff

    def get_rebate_status(self, sn_color):
        rebate_status = sn_color
        if sn_color == "green":
            rebate_status = "tgreen"
        elif sn_color == "green1":
            rebate_status = "green"

        return rebate_status

    def convet_measure_staff(self, staff, pay_time):
        buy_data = datetime.datetime(pay_time.year, pay_time.month, pay_time.day)
        measure_staff_qs = MeasureStaff.search(staff = staff, report_date = buy_data)
        if measure_staff_qs.count() == 0:
            MeasureStaff.create(staff = staff, report_date = buy_data)
