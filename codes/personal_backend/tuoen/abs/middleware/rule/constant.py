# coding=UTF-8

from tuoen.abs.middleware.rule.base import BaseRule
from tuoen.abs.middleware.rule.entity import RuleEntity


class Action(object):
    QUERY = ("query", "查询")
    MODELQUERY = ("modelquery", "型号查询")
    ADD = ("add", "添加")
    MODELADD = ("modeladd", "型号添加")
    EDIT = ("edit", "编辑")
    MODELEDIT = ("modeledit", "型号编辑")
    SNEDIT = ("snedit", "SN编辑")
    CHANGEEDIT = ("change", "补换货编辑")
    DELETE = ("delete", "删除")
    REMOVEDELETE = ("returns", "退货")
    MODELDELETE = ("modeldelete", "删除型号")
    UPLOAD = ("upload", "上传")
    CONVERT = ("convert", "转化")
    ALLOT = ("allot", "分配")
    ADDEVENT = ("addevent", "添加事件")
    RESET = ("reset", "狀態重置")
    TRANSFER = ("transfer", "转移")
    RECOVER = ("recover", "恢复")
    EXECUTED = ("executed", "执行")
    APPLY = ("apply", "申请补货")
    EXPORT = ("export", "导出")


class Permise(BaseRule):
    DEFAULT = RuleEntity("permise", "权限管理")

    DEFAULT_DEPARTMENT = RuleEntity("department", "部门管理")
    DEFAULT_DEPARTMENT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_DEPARTMENT_ADD = RuleEntity(*Action.ADD)
    DEFAULT_DEPARTMENT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_DEPARTMENT_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_ROLE = RuleEntity("role", "角色管理")
    DEFAULT_ROLE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ROLE_ADD = RuleEntity(*Action.ADD)
    DEFAULT_ROLE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_ROLE_DEL = RuleEntity(*Action.DELETE)


class Staff(BaseRule):
    DEFAULT = RuleEntity("staff", "员工管理")

    DEFAULT_ROSTER = RuleEntity("roster", "花名册")
    DEFAULT_ROSTER_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ROSTER_ADD = RuleEntity(*Action.ADD)
    DEFAULT_ROSTER_EDIT = RuleEntity(*Action.EDIT)

    DEFAULT_STAFF = RuleEntity("staff", "员工列表")
    DEFAULT_STAFF_QUERY = RuleEntity(*Action.QUERY)

    DEFAULT_STAFFALIAS = RuleEntity("staffalias", "别名管理")
    DEFAULT_STAFFALIAS_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_STAFFALIAS_ADD = RuleEntity(*Action.ADD)
    DEFAULT_STAFFALIAS_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_STAFFALIAS_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_DEPARTMENTCHANGE = RuleEntity("departmentchange", "部门调岗管理")
    DEFAULT_DEPARTMENTCHANGE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_DEPARTMENTCHANGE_ADD = RuleEntity(*Action.ADD)
    DEFAULT_DEPARTMENTCHANGE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_DEPARTMENTCHANGE_DEL = RuleEntity(*Action.DELETE)
    DEFAULT_DEPARTMENTCHANGE_EXECUTED = RuleEntity(*Action.EXECUTED)

class Order(BaseRule):
    DEFAULT = RuleEntity("order", "订单管理")

    DEFAULT_ORDER = RuleEntity("order", "订单列表")
    DEFAULT_ORDER_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ORDER_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_ORDER_APPLY = RuleEntity(*Action.APPLY)
    DEFAULT_ORDER_TRANSFER = RuleEntity(*Action.TRANSFER)

    DEFAULT_ORDERRETURNS = RuleEntity("returns", "退货单列表")
    DEFAULT_ORDERRETURNS_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ORDERRETURNS_REMOVE = RuleEntity(*Action.REMOVEDELETE)
    DEFAULT_ORDERRETURNS_ADD = RuleEntity(*Action.ADD)
    DEFAULT_ORDERRETURNS_RECOVER = RuleEntity(*Action.RECOVER)

    DEFAULT_ORDERREPLENISHMENT = RuleEntity("replenishment", "补货单列表")
    DEFAULT_ORDERREPLENISHMENT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ORDERREPLENISHMENT_DELETE = RuleEntity(*Action.DELETE)
    DEFAULT_ORDERREPLENISHMENT_EXPORT = RuleEntity(*Action.EXPORT)

class Mobile(BaseRule):
    DEFAULT = RuleEntity("mobile", "手机管理")

    DEFAULT_MOBILEDEVICES = RuleEntity("mobiledevices", "手机设备")
    DEFAULT_MOBILEDEVICES_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MOBILEDEVICES_ADD = RuleEntity(*Action.ADD)
    DEFAULT_MOBILEDEVICES_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MOBILEDEVICES_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_MOBILEPHONE = RuleEntity("mobilephone", "号码管理")
    DEFAULT_MOBILEPHONE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MOBILEPHONE_ADD = RuleEntity(*Action.ADD)
    DEFAULT_MOBILEPHONE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MOBILEPHONE_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_MOBILETAINTAIN = RuleEntity("mobilemaintain", "设备维护")
    DEFAULT_MOBILETAINTAIN_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MOBILETAINTAIN_ADD = RuleEntity(*Action.ADD)
    DEFAULT_MOBILETAINTAIN_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MOBILETAINTAIN_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_WECHAT = RuleEntity("wechat", "微信手机盘点")
    DEFAULT_WECHAT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_WECHAT_ADD = RuleEntity(*Action.ADD)
    DEFAULT_WECHAT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_WECHAT_DEL = RuleEntity(*Action.DELETE)

class Customer(BaseRule):
    DEFAULT = RuleEntity("customer", "客户管理")

    DEFAULT_CUSTOMER = RuleEntity("customer", "客户列表")
    DEFAULT_CUSTOMER_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_CUSTOMER_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_CUSTOMER_ALLOT = RuleEntity(*Action.ALLOT)

    DEFAULT_CUSREGISTER = RuleEntity("customerregister", "客户註冊列表")
    DEFAULT_CUSREGISTER_QUERY = RuleEntity(*Action.QUERY)

    DEFAULT_CUSTOMERREBATE = RuleEntity('customerrabate', "客戶返利")
    DEFAULT_CUSTOMERREBATE_QUERY = RuleEntity(*Action.QUERY)

    DEFAULT_CUSTOMERTRANSACTION = RuleEntity('customertransaction', "客戶流水")
    DEFAULT_CUSTOMERTRANSACTION_QUERY = RuleEntity(*Action.QUERY)

class SaleChance(BaseRule):
    DEFAULT = RuleEntity("salechance", "销售机会")

    DEFAULT_SALECHANCE = RuleEntity("salechance", "机会列表")
    DEFAULT_SALECHANCE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_SALECHANCE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_SALECHANCE_ADDTRACK = RuleEntity(*Action.ADDEVENT)

class ServiceItem(BaseRule):
    DEFAULT = RuleEntity("serviceitem", "设备管理")

    DEFAULT_SERVICEITEM = RuleEntity("serviceitem", "设备管理")
    DEFAULT_SERVICEITEM_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_SERVICEITEM_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_SERVICEITEM_SNEDIT = RuleEntity(*Action.SNEDIT)

    DEFAULT_QUALITY = RuleEntity("device", "设备质检")
    DEFAULT_QUALITY_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_QUALITY_REMOVEDELETE = RuleEntity(*Action.REMOVEDELETE)
    DEFAULT_QUALITY_CHANGEEDIT = RuleEntity(*Action.CHANGEEDIT)
    # DEFAULT_REMOVE = RuleEntity("remove", "退货")
    DEFAULT_SERVICEITEM_REMOVEDELETE = RuleEntity(*Action.REMOVEDELETE)

    # DEFAULT_CHANGE = RuleEntity("change", "换补货标记")
    DEFAULT_SERVICEITEM_CHANGEEDIT = RuleEntity(*Action.CHANGEEDIT)

    DEFAULT_DEPTDEV = RuleEntity("deptdev", "部门设备")
    DEFAULT_DEPTDEV_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_DEPTDEV_EDIT = RuleEntity(*Action.EDIT)

class Shop(BaseRule):
    DEFAULT = RuleEntity("shop", "店铺管理")

    DEFAULT_CHANNEL = RuleEntity("channel", "店铺渠道管理")
    DEFAULT_CHANNEL_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_CHANNEL_ADD = RuleEntity(*Action.ADD)
    DEFAULT_CHANNEL_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_CHANNEL_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_SHOP = RuleEntity("shop", "店铺管理")
    DEFAULT_SHOP_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_SHOP_ADD = RuleEntity(*Action.ADD)
    DEFAULT_SHOP_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_SHOP_DEL = RuleEntity(*Action.DELETE)

class Measure(BaseRule):
    DEFAULT = RuleEntity("measure", "绩效管理")

    DEFAULT_MEASURESHOP = RuleEntity("measureshop", "店铺绩效")
    DEFAULT_MEASURESHOP_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MEASURESHOP_ADD = RuleEntity(*Action.ADD)
    DEFAULT_MEASURESHOP_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MEASURESHOP_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_MEASURESTAFF = RuleEntity("measurestaff", "员工绩效")
    DEFAULT_MEASURESTAFF_QUERY = RuleEntity(*Action.QUERY)

    DEFAULT_MEASUREDEPARTMENT = RuleEntity("measuredepartment", "部门绩效")
    DEFAULT_MEASUREDEPARTMENT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MEASUREDEPARTMENT_ADD = RuleEntity(*Action.ADD)
    DEFAULT_MEASUREDEPARTMENT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MEASUREDEPARTMENT_DEL = RuleEntity(*Action.DELETE)

    DEFAULT_STATISTICS = RuleEntity("statistics", "员工绩效统计")
    DEFAULT_STATISTICS_QUERY = RuleEntity(*Action.QUERY)

    DEFAULT_PERFORMANCE = RuleEntity('performance', "业绩统计")
    DEFAULT_PERFORMANCE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_PERFORMANCE_EXPORT = RuleEntity(*Action.EXPORT)

class DataImport(BaseRule):
    DEFAULT = RuleEntity("dataimport", "数据导入")

    DEFAULT_BUYINFO = RuleEntity("buyinfo", "购买信息")
    DEFAULT_BUYINFO_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_BUYINFO_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_BUYINFO_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_BUYINFO_CONVERT = RuleEntity(*Action.CONVERT)
    DEFAULT_BUYINFO_DELETE = RuleEntity(*Action.DELETE)
    DEFAULT_BUYINFO_RESET = RuleEntity(*Action.RESET)

    DEFAULT_EQUIPMENTIN = RuleEntity("equipmentin", "设备入库")
    DEFAULT_EQUIPMENTIN_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_EQUIPMENTIN_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_EQUIPMENTIN_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_EQUIPMENTIN_CONVERT = RuleEntity(*Action.CONVERT)
    DEFAULT_EQUIPMENTIN_RESET = RuleEntity(*Action.RESET)

    DEFAULT_EQUIPMENTOUT = RuleEntity("equipmentout", "设备出库")
    DEFAULT_EQUIPMENTOUT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_EQUIPMENTOUT_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_EQUIPMENTOUT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_EQUIPMENTOUT_CONVERT = RuleEntity(*Action.CONVERT)
    DEFAULT_EQUIPMENTOUT_RESET = RuleEntity(*Action.RESET)

    DEFAULT_REGISTER = RuleEntity("register", "客户注册")
    DEFAULT_REGISTER_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_REGISTER_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_REGISTER_CONVERT = RuleEntity(*Action.CONVERT)
    DEFAULT_REGISTER_RESET = RuleEntity(*Action.RESET)

    DEFAULT_REBATE = RuleEntity("rebate", "客户返利")
    DEFAULT_REBATE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_REBATE_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_REBATE_CONVERT = RuleEntity(*Action.CONVERT)
    DEFAULT_REBATE_RESET = RuleEntity(*Action.RESET)

    DEFAULT_TRANSACTION = RuleEntity("transaction", "交易流水")
    DEFAULT_TRANSACTION_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_TRANSACTION_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_TRANSACTION_CONVERT = RuleEntity(*Action.CONVERT)
    DEFAULT_TRANSACTION_RESET = RuleEntity(*Action.RESET)

    DEFAULT_STAFFIMPORT = RuleEntity("staffimport", "员工导入")
    DEFAULT_STAFFIMPORT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_STAFFIMPORT_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_STAFFIMPORT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_STAFFIMPORT_CONVERT = RuleEntity(*Action.CONVERT)
    DEFAULT_STAFFIMPORT_RESET = RuleEntity(*Action.RESET)

    DEFAULT_MOBILEDEVICES = RuleEntity("mobiledevices", "手机设备")
    DEFAULT_MOBILEDEVICES_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MOBILEDEVICES_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_MOBILEDEVICES_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MOBILEDEVICES_CONVERT = RuleEntity(*Action.CONVERT)
    DEFAULT_MOBILEDEVICES_RESET = RuleEntity(*Action.RESET)

    DEFAULT_MOBILEPHONE = RuleEntity("mobilephone", "手机号码")
    DEFAULT_MOBILEPHONE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_MOBILEPHONE_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_MOBILEPHONE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_MOBILEPHONE_CONVERT = RuleEntity(*Action.CONVERT)
    DEFAULT_MOBILEPHONE_RESET = RuleEntity(*Action.RESET)


    DEFAULT_RETURNS = RuleEntity("returns", "退貨單")
    DEFAULT_RETURNS_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_RETURNS_UPLOAD = RuleEntity(*Action.UPLOAD)
    DEFAULT_RETURNS_CONVERT = RuleEntity(*Action.CONVERT)
    DEFAULT_RETURNS_RESET = RuleEntity(*Action.RESET)

class Product(BaseRule):
    DEFAULT = RuleEntity("product", "产品管理")

    DEFAULT_PRODUCT = RuleEntity("product", "产品列表")
    DEFAULT_PRODUCT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_PRODUCT_ADD = RuleEntity(*Action.ADD)
    DEFAULT_PRODUCT_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_PRODUCT_DEL = RuleEntity(*Action.DELETE)

    # DEFAULT_PRODUCTMODEL = RuleEntity("productmodel", "型号管理")
    DEFAULT_PRODUCT_MODELQUERY = RuleEntity(*Action.MODELQUERY)
    DEFAULT_PRODUCT_MODELADD = RuleEntity(*Action.MODELADD)
    DEFAULT_PRODUCT_MODELEDIT = RuleEntity(*Action.MODELEDIT)
    DEFAULT_PRODUCT_MODELDEL = RuleEntity(*Action.MODELDELETE)

    DEFAULT_EQUIPMENTIN = RuleEntity("inequipment", "設備入庫")
    DEFAULT_EQUIPMENTIN_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_EQUIPMENTIN_EDIT = RuleEntity(*Action.EDIT)

    DEFAULT_EQUIPMENTOUT = RuleEntity("outequipment", "設備出庫")
    DEFAULT_EQUIPMENTOUT_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_EQUIPMENTOUT_EDIT = RuleEntity(*Action.EDIT)


permise_rules = Permise()
staff_rules = Staff()
order_rules = Order()
mobile_rules = Mobile()
customer_rules = Customer()
sale_chance_rules = SaleChance()
service_item_rules = ServiceItem()
shop_rules = Shop()
measure_rules = Measure()
data_import_rules = DataImport()
product_rules = Product()
