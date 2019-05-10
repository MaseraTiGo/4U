# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_shop import Shop


class ImportStatus(object):
    INIT = "init"
    EXCUTTING = "excutting"
    FINISH = "finish"
    FAILED = "failed"

    CHOICES = ((INIT, "初始化"), (EXCUTTING, "执行中"), (FINISH, "已完成"), (FAILED, "失败"))


class BaseImport(BaseModel):

    status = CharField(verbose_name = "执行状态", max_length = 24, choices = ImportStatus.CHOICES, default = ImportStatus.INIT)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    error_text = TextField(verbose_name = "转化失败描述", null = True, default = "")

    class Meta:
        abstract = True
    @classmethod
    def search(cls, **attrs):
        order_qs = cls.query().filter(**attrs)
        return order_qs

class ImportCustomerRegister(BaseImport):
    """设备注册表"""
    agent_name = CharField(verbose_name = "代理商名称", max_length = 64, default = "")
    code = CharField(verbose_name = "客户编码", max_length = 32, default = "")
    phone = CharField(verbose_name = "注册手机号", max_length = 32, default = "")
    name = CharField(verbose_name = "客户姓名", max_length = 64, default = "")
    register_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)
    bind_time = DateTimeField(verbose_name = "绑定时间", default = timezone.now)
    device_code = CharField(verbose_name = "设备编码", max_length = 32, default = "")


class ImportCustomerRebate(BaseImport):
    """返利表"""
    agent_id = CharField(verbose_name = "代理商ID", max_length = 64, default = "", null = True)
    agent_name = CharField(verbose_name = "代理商名称", max_length = 32, default = "", null = True)
    code = CharField(verbose_name = "客户编码", max_length = 32, default = "", null = True)
    name = CharField(verbose_name = "客户名称", max_length = 64, default = "", null = True)
    phone = CharField(verbose_name = "注册手机号", max_length = 32, default = "", null = True)
    activity_type = CharField(verbose_name = "活动类型", max_length = 32, null = True)
    is_silent = CharField(verbose_name = "是否为沉默用户", max_length = 32, null = True)
    device_code = CharField(verbose_name = "设备编码", max_length = 32, null = True)

    register_time = DateTimeField(verbose_name = "注册时间", null = True)
    bind_time = DateTimeField(verbose_name = "绑定时间", null = True)
    month = DateField(verbose_name = "交易月份", null = True)
    transaction_amount = IntegerField(verbose_name = "交易金额/分", default = 0)
    effective_amount = IntegerField(verbose_name = "有效金额/分", default = 0)
    accumulate_amount = IntegerField(verbose_name = "当月累计交易金额/分", default = 0)
    history_amount = IntegerField(verbose_name = "历史累计交易金额/分", default = 0)
    type = CharField(verbose_name = "号段类型", max_length = 32, null = True)
    is_rebate = CharField(verbose_name = "是否返利", max_length = 32, default = "")
    remark = TextField(verbose_name = "备注")
    activation_date = DateField(verbose_name = "激活日期", null = True)


class ImportCustomerTransaction(BaseImport):
    """交易流水表"""

    agent_name = CharField(verbose_name = "代理商名称", max_length = 32, default = "", null = True)
    service_code = CharField(verbose_name = "服务编码", max_length = 32, default = "", null = True)
    code = CharField(verbose_name = "客户编码", max_length = 64, default = "", null = True)
    phone = CharField(verbose_name = "注册手机号", max_length = 32, default = "", null = True)

    transaction_year = DateField(verbose_name = "交易日期", null = True)
    transaction_day = CharField(verbose_name = "交易时间", max_length = 32, default = "", null = True)
    transaction_code = CharField(verbose_name = "交易流水号", max_length = 32, default = "", null = True)
    transaction_money = IntegerField(verbose_name = "交易金额/分", default = 0)
    fee = IntegerField(verbose_name = "手续费/分", default = 0)
    good_service_fee = IntegerField(verbose_name = "优享手续费/分", default = 0)
    rate = IntegerField(verbose_name = "客户费率", default = 0)
    good_service_rate = IntegerField(verbose_name = "优享费率", default = 0)
    other_fee = IntegerField(verbose_name = "其它手续费/分", default = 0)
    transaction_status = CharField(verbose_name = "交易状态", max_length = 64, default = "", null = True)
    type = CharField(verbose_name = "号段类型", max_length = 64, default = "")



class ImportCustomerBuyinfo(BaseImport):
    """购买信息"""

    serial_number = IntegerField(verbose_name = "序号", default = 0, null = True)
    order_sn = CharField(verbose_name = "订单编号", max_length = 64, default = "", null = True)
    goods_sn = CharField(verbose_name = "商品编号", max_length = 64, default = "", null = True)
    buy_number = IntegerField(verbose_name = "购买数量", default = 0, null = True)
    buy_money = IntegerField(verbose_name = "订单金额/分", default = 0, null = True)
    pay_time = DateTimeField(verbose_name = "付款时间", null = True)
    shop_name = CharField(verbose_name = "网点名称", max_length = 64, default = "", null = True)
    buy_name = CharField(verbose_name = "买家姓名", max_length = 32, default = "", null = True)
    province = CharField(verbose_name = "省", max_length = 32, default = "", null = True)
    city = CharField(verbose_name = "市", max_length = 32, default = "", null = True)
    area = CharField(verbose_name = "区", max_length = 32, default = "", null = True)
    address = TextField(verbose_name = "详细地址", max_length = 32, default = "", null = True)
    logistics_company = CharField(verbose_name = "物流公司", max_length = 32, default = "", null = True)
    logistics_code = CharField(verbose_name = "物流单号", max_length = 32, default = "", null = True)
    buy_phone = CharField(verbose_name = "联系方式", max_length = 128, default = "", null = True)
    remark = TextField(verbose_name = "客服备注", max_length = 32, default = "", null = True)
    buy_nick = CharField(verbose_name = "卖家账号", max_length = 32, default = "", null = True)
    device_code = CharField(verbose_name = "设备编码", max_length = 32, default = "", null = True)


class ImportEquipmentIn(BaseImport):
    """SN设备入库信息"""

    add_time = DateField(verbose_name = "添加时间", max_length = 20, null = True, blank = True)
    agent_name = CharField(verbose_name = "代理商名称", max_length = 32, default = "")
    product_type = CharField(verbose_name = "产品类型", max_length = 32, default = "")
    product_model = CharField(verbose_name = "产品型号", max_length = 32, default = "")
    min_number = BigIntegerField (verbose_name = "起始号段")
    max_number = BigIntegerField (verbose_name = "终止号段")
    quantity = IntegerField(verbose_name = "入库数量", default = 0)
    remark = TextField(verbose_name = "到货备注", max_length = 128, default = "")


class ImportEquipmentOut(BaseImport):
    """SN设备出库信息"""

    add_time = DateField(verbose_name = "添加时间", max_length = 20, null = True, blank = True)
    agent_name = CharField(verbose_name = "代理商名称", max_length = 32, default = "")
    agent_phone = CharField(verbose_name = "代理商电话", max_length = 20, default = "")
    product_type = CharField(verbose_name = "产品类型", max_length = 32, default = "")
    product_model = CharField(verbose_name = "产品型号", max_length = 32, default = "")
    min_number = BigIntegerField (verbose_name = "起始号段")
    max_number = BigIntegerField (verbose_name = "终止号段")
    quantity = IntegerField(verbose_name = "入库数量", default = 0)
    price = CharField(verbose_name = "单价", max_length = 32, default = "")
    salesman = CharField(verbose_name = "业务员", max_length = 32, default = "")
    address = CharField(verbose_name = "发货地址", max_length = 128, default = "")
    rate = CharField(verbose_name = "签约费率", max_length = 32, default = "")
    remark = TextField(verbose_name = "出货备注", max_length = 128, default = "")
    type = CharField(verbose_name = "出库类型", max_length = 32, default = "")


class ImportStaff(BaseImport):
    """员工信息"""
    name = CharField(verbose_name = "姓名", max_length = 64, default = "")
    position = CharField(verbose_name = "职位", max_length = 64, default = "")
    department = CharField(verbose_name = "部门", max_length = 128, default = "")
    phone = CharField(verbose_name = "手机号", max_length = 20, default = "")
    gender = CharField(verbose_name = "性别", max_length = 24, default = "")
    identity = CharField(verbose_name = "身份证号", max_length = 24, default = "")
    birthday = DateField(verbose_name = "生日", null = True, blank = True)
    age = IntegerField(verbose_name = "年龄", default = 0)
    emergency_contact = CharField(verbose_name = "紧急联系人", max_length = 64, default = "")
    emergency_phone = CharField(verbose_name = "紧急联系人电话", max_length = 20, default = "")
    address = TextField(verbose_name = "详细地址", default = "")
    entry_time = DateField(verbose_name = "入职时间", null = True, blank = True)
    education = CharField(verbose_name = "学历", max_length = 24, default = "")
    bank_number = CharField(verbose_name = "招行卡号", max_length = 32, default = "")
    contract_b = CharField(verbose_name = "合同编号（必）", max_length = 64, default = "")
    contract_l = CharField(verbose_name = "合同编号（立）", max_length = 64, default = "")
    expire_time = DateField(verbose_name = "到期时间", null = True, blank = True)
    is_on_job = CharField(verbose_name = "是否在职", max_length = 64, default = "")
    quit_time = DateField(verbose_name = "离职时间", null = True, blank = True)
    remark = TextField(verbose_name = "备注", default = "")


class ImportMobileDevices(BaseImport):
    """手机设备表信息"""
    group_leader = CharField(verbose_name = "组长姓名", max_length = 64, default = "")
    mobile_code = CharField(verbose_name = "手机编号", max_length = 64, default = "")
    group_member = CharField(verbose_name = "组员姓名", max_length = 64, default = "")
    wechat_nick = CharField(verbose_name = "微信昵称", max_length = 64, default = "")
    wechat_number = CharField(verbose_name = "微信号", max_length = 128, default = "")
    wechat_password = CharField(verbose_name = "微信密码", max_length = 128, default = "")
    pay_password = CharField(verbose_name = "微信支付密码", max_length = 64, default = "")
    wechat_remark = CharField(verbose_name = "微信号备注", max_length = 64, default = "")
    department = CharField(verbose_name = "部门", max_length = 64, default = "")
    phone_number = CharField(verbose_name = "手机号", max_length = 64, default = "")
    operator = CharField(verbose_name = "运营商", max_length = 64, default = "")
    real_name = CharField(verbose_name = "实名人姓名", max_length = 64, default = "")
    phone_remark = TextField(verbose_name = "手机号备注", default = "")
    flow_card_number = CharField(verbose_name = "流量卡号", max_length = 128, default = "")
    imei = CharField(verbose_name = "手机imei号", max_length = 128, default = "")
    brand = CharField(verbose_name = "手机品牌", max_length = 64, default = "")
    model = CharField(verbose_name = "手机型号", max_length = 64, default = "")
    price = IntegerField(verbose_name = "购买价格/分", default = 0)
    mobile_status = CharField(verbose_name = "手机设备状态", max_length = 32, default = "")
    mobile_remark = TextField(verbose_name = "手机设备备注", default = "")
    phone_change = TextField(verbose_name = "手机变更信息", default = "")


class ImportMobilePhone(BaseImport):
    """手机号码信息"""
    name = CharField(verbose_name = "姓名", max_length = 64, default = "")
    identity = CharField(verbose_name = "身份证号", max_length = 64, default = "")
    phone_number = CharField(verbose_name = "手机号", max_length = 64, default = "")
    department = CharField(verbose_name = "部门", max_length = 64, default = "")
    is_working = CharField(verbose_name = "在职情况", max_length = 128, default = "")
    card_password = CharField(verbose_name = "手机卡密码", max_length = 128, default = "")
    operator = CharField(verbose_name = "运营商", max_length = 64, default = "")
    rent = IntegerField(verbose_name = "月租", default = 0)
    phone_status = CharField(verbose_name = "手机号状态", max_length = 64, default = "")
    phone_remark = CharField(verbose_name = "手机号备注", max_length = 64, default = "")

class ImportReturns(BaseImport):
    "退貨信息"
    code = CharField(verbose_name = "设备SN码", max_length = 64, default = "")
