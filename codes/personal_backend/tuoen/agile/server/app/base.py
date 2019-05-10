# coding=UTF-8

from tuoen.sys.core.service.base import BaseAPIService
from tuoen.abs.middleware.rule import rule_register, permise_rules, staff_rules, \
    order_rules, mobile_rules, customer_rules, sale_chance_rules, \
    shop_rules, service_item_rules, measure_rules, data_import_rules, \
    product_rules

from tuoen.agile.apis import test


class UserService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "用户服务"

    @classmethod
    def get_desc(self):
        return "针对注册登录用户提供服务"

    @classmethod
    def get_flag(cls):
        return "user"


user_service = UserService()
from tuoen.agile.apis.account.staff import Login, Generate

user_service.add(Login, Generate)

from tuoen.agile.apis.account.staff.update import Password

user_service.add(Password)

from tuoen.agile.apis.user.staff import Add, Get, Update, Search, SearchAll, UpdateByAdmin, GetByadmin, Match, \
    SearchAllFaker, Roster, InputWorkTime, PositionTransfer

user_service.add(Add, Get, Update, Search, SearchAll, UpdateByAdmin, GetByadmin, Match, SearchAllFaker, Roster,
                 InputWorkTime, PositionTransfer)
rule_register.register_api(staff_rules.DEFAULT_ROSTER_QUERY, Roster)
rule_register.register_api(staff_rules.DEFAULT_ROSTER_EDIT, GetByadmin, UpdateByAdmin, InputWorkTime)
rule_register.register_api(staff_rules.DEFAULT_ROSTER_ADD, Add)
rule_register.register_api(staff_rules.DEFAULT_STAFF_QUERY, Search)

from tuoen.agile.apis.user.token import Renew

user_service.add(Renew)

from tuoen.agile.apis.journal import Search

user_service.add(Search)

from tuoen.agile.apis.permise.staff.role import Add, List, Update, Remove, Get

user_service.add(Add, List, Update, Remove, Get)
rule_register.register_api(permise_rules.DEFAULT_ROLE_QUERY, List)
rule_register.register_api(permise_rules.DEFAULT_ROLE_ADD, Add)
rule_register.register_api(permise_rules.DEFAULT_ROLE_EDIT, Get, Update)
rule_register.register_api(permise_rules.DEFAULT_ROLE_DEL, Remove)

from tuoen.agile.apis.permise.staff.rule import List

user_service.add(List)

from tuoen.agile.apis.permise.staff.department import Add, List, Update, Remove, Get

user_service.add(Add, List, Update, Remove, Get)
rule_register.register_api(permise_rules.DEFAULT_DEPARTMENT_QUERY, List)
rule_register.register_api(permise_rules.DEFAULT_DEPARTMENT_ADD, Add)
rule_register.register_api(permise_rules.DEFAULT_DEPARTMENT_EDIT, Get, Update)
rule_register.register_api(permise_rules.DEFAULT_DEPARTMENT_DEL, Remove)

from tuoen.agile.apis.mobile.devices import Add, Search, Searchall, Get, Update, Remove

user_service.add(Add, Search, Searchall, Get, Update, Remove)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEDEVICES_QUERY, Search)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEDEVICES_ADD, Add)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEDEVICES_EDIT, Get, Update)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEDEVICES_DEL, Remove)

from tuoen.agile.apis.mobile.phone import Add, Search, Get, Update, Remove

user_service.add(Add, Search, Get, Update, Remove)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEPHONE_QUERY, Search)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEPHONE_ADD, Add)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEPHONE_EDIT, Get, Update)
rule_register.register_api(mobile_rules.DEFAULT_MOBILEPHONE_DEL, Remove)

from tuoen.agile.apis.mobile.maintain import Add, Search, Get, Update, Remove

user_service.add(Add, Search, Get, Update, Remove)
rule_register.register_api(mobile_rules.DEFAULT_MOBILETAINTAIN_QUERY, Search)
rule_register.register_api(mobile_rules.DEFAULT_MOBILETAINTAIN_ADD, Add)
rule_register.register_api(mobile_rules.DEFAULT_MOBILETAINTAIN_EDIT, Get, Update)
rule_register.register_api(mobile_rules.DEFAULT_MOBILETAINTAIN_DEL, Remove)

from tuoen.agile.apis.shop.channel import Add, Search, Get, Update, Remove, Match, SearchAll

user_service.add(Add, Search, Get, Update, Remove, Match, SearchAll)
rule_register.register_api(shop_rules.DEFAULT_CHANNEL_QUERY, Search)
rule_register.register_api(shop_rules.DEFAULT_CHANNEL_ADD, Add)
rule_register.register_api(shop_rules.DEFAULT_CHANNEL_EDIT, Get, Update)
rule_register.register_api(shop_rules.DEFAULT_CHANNEL_DEL, Remove)

from tuoen.agile.apis.shop import Add, Search, Get, Update, Remove, Match, SearchAll

user_service.add(Add, Search, Get, Update, Remove, Match, SearchAll)

rule_register.register_api(shop_rules.DEFAULT_SHOP_QUERY, Search)
rule_register.register_api(shop_rules.DEFAULT_SHOP_ADD, Add)
rule_register.register_api(shop_rules.DEFAULT_SHOP_EDIT, Get, Update)
rule_register.register_api(shop_rules.DEFAULT_SHOP_DEL, Remove)

from tuoen.agile.apis.shop.goods import Search, SearchAll, Match

user_service.add(Search, SearchAll, Match)

from tuoen.agile.apis.order import Search, Get, Transfer, ApplyForReplenishment

user_service.add(Search, Get, Transfer, ApplyForReplenishment)
rule_register.register_api(order_rules.DEFAULT_ORDER_QUERY, Search)
rule_register.register_api(order_rules.DEFAULT_ORDER_EDIT, Get)
rule_register.register_api(order_rules.DEFAULT_ORDER_TRANSFER, Transfer)
rule_register.register_api(order_rules.DEFAULT_ORDER_APPLY, ApplyForReplenishment)

from tuoen.agile.apis.measure.shop import Add, Search, Get, Update, Remove, Statistics

user_service.add(Add, Search, Get, Update, Remove, Statistics)
rule_register.register_api(measure_rules.DEFAULT_MEASURESHOP_QUERY, Search)
rule_register.register_api(measure_rules.DEFAULT_MEASURESHOP_ADD, Add)
rule_register.register_api(measure_rules.DEFAULT_MEASURESHOP_EDIT, Get, Update)
rule_register.register_api(measure_rules.DEFAULT_MEASURESHOP_DEL, Remove)

from tuoen.agile.apis.measure.staff import Add, Search, Get, Update, Remove, Statistics

user_service.add(Add, Search, Get, Update, Remove, Statistics)
rule_register.register_api(measure_rules.DEFAULT_MEASURESTAFF_QUERY, Search)
rule_register.register_api(measure_rules.DEFAULT_MEASUREDEPARTMENT_ADD, Add)
rule_register.register_api(measure_rules.DEFAULT_MEASUREDEPARTMENT_EDIT, Get, Update)
rule_register.register_api(measure_rules.DEFAULT_MEASUREDEPARTMENT_DEL, Remove)

from tuoen.agile.apis.measure.staff.department import Search

user_service.add(Search)
rule_register.register_api(measure_rules.DEFAULT_MEASUREDEPARTMENT_QUERY, Search)

from tuoen.agile.apis.measure import Statistics

user_service.add(Statistics)
rule_register.register_api(measure_rules.DEFAULT_STATISTICS_QUERY, Statistics)

from tuoen.agile.apis.service.item import Search, Statistics, Get, EditSn

user_service.add(Search, Statistics, Get, EditSn)
rule_register.register_api(service_item_rules.DEFAULT_SERVICEITEM_QUERY, Search, Statistics)
rule_register.register_api(service_item_rules.DEFAULT_SERVICEITEM_EDIT, Get)
rule_register.register_api(service_item_rules.DEFAULT_SERVICEITEM_SNEDIT, EditSn)

from tuoen.agile.apis.customer import Search, Get, Update

user_service.add(Search, Get, Update)
rule_register.register_api(customer_rules.DEFAULT_CUSTOMER_QUERY, Search)
rule_register.register_api(customer_rules.DEFAULT_CUSTOMER_EDIT, Get, Update)
rule_register.register_api(service_item_rules.DEFAULT_SERVICEITEM_EDIT, Update)

from tuoen.agile.apis.customer.sale.chance import Add, Search, Update

user_service.add(Add, Search, Update)
rule_register.register_api(customer_rules.DEFAULT_CUSTOMER_ALLOT, Add)
rule_register.register_api(sale_chance_rules.DEFAULT_SALECHANCE_QUERY, Search)
rule_register.register_api(sale_chance_rules.DEFAULT_SALECHANCE_EDIT, Update)
rule_register.register_api(customer_rules.DEFAULT_CUSTOMER_EDIT, Search)

from tuoen.agile.apis.event.track import Add, Search, SearchByTrack

user_service.add(Add, Search, SearchByTrack)
rule_register.register_api(sale_chance_rules.DEFAULT_SALECHANCE_QUERY, SearchByTrack)
rule_register.register_api(sale_chance_rules.DEFAULT_SALECHANCE_ADDTRACK, Add)

# data import
from tuoen.agile.apis.data.register import Upload, Search, Convert, ResetStatus

user_service.add(Upload, Search, Convert, ResetStatus)
rule_register.register_api(data_import_rules.DEFAULT_REGISTER_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_REGISTER_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_REGISTER_CONVERT, Convert)
rule_register.register_api(data_import_rules.DEFAULT_REGISTER_RESET, ResetStatus)

# data import
from tuoen.agile.apis.data.rebate import Upload, Search, Convert, ResetStatus

user_service.add(Upload, Search, Convert, ResetStatus)
rule_register.register_api(data_import_rules.DEFAULT_REBATE_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_REBATE_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_REBATE_CONVERT, Convert)
rule_register.register_api(data_import_rules.DEFAULT_REBATE_RESET, ResetStatus)

# data import
from tuoen.agile.apis.data.transaction import Upload, Search, Convert, ResetStatus

user_service.add(Upload, Search, Convert, ResetStatus)
rule_register.register_api(data_import_rules.DEFAULT_TRANSACTION_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_TRANSACTION_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_TRANSACTION_CONVERT, Convert)
rule_register.register_api(data_import_rules.DEFAULT_TRANSACTION_RESET, ResetStatus)

# data import
from tuoen.agile.apis.data.buyinfo import Upload, Search, Convert, Update, Remove, ResetStatus

user_service.add(Upload, Search, Convert, Update, Remove, ResetStatus)
rule_register.register_api(data_import_rules.DEFAULT_BUYINFO_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_BUYINFO_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_BUYINFO_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_BUYINFO_CONVERT, Convert)
rule_register.register_api(data_import_rules.DEFAULT_BUYINFO_DELETE, Remove)
rule_register.register_api(data_import_rules.DEFAULT_BUYINFO_RESET, ResetStatus)

# data import
from tuoen.agile.apis.data.equipmentin import Upload, Search, Convert, Update, ResetStatus

user_service.add(Upload, Search, Convert, Update, ResetStatus)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTIN_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTIN_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTIN_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTIN_CONVERT, Convert)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTIN_RESET, ResetStatus)

# data import
from tuoen.agile.apis.data.equipmentout import Upload, Search, Convert, Update, ResetStatus

user_service.add(Upload, Search, Convert, Update, ResetStatus)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTOUT_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTOUT_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTOUT_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTOUT_CONVERT, Convert)
rule_register.register_api(data_import_rules.DEFAULT_EQUIPMENTOUT_RESET, ResetStatus)

# data import
from tuoen.agile.apis.data.staff import Upload, Search, Convert, Update, ResetStatus

user_service.add(Upload, Search, Convert, Update, ResetStatus)
rule_register.register_api(data_import_rules.DEFAULT_STAFFIMPORT_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_STAFFIMPORT_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_STAFFIMPORT_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_STAFFIMPORT_CONVERT, Convert)
rule_register.register_api(data_import_rules.DEFAULT_STAFFIMPORT_RESET, ResetStatus)

# data import
from tuoen.agile.apis.data.mobiledevices import Upload, Search, Convert, Update, ResetStatus

user_service.add(Upload, Search, Convert, Update, ResetStatus)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEDEVICES_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEDEVICES_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEDEVICES_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEDEVICES_CONVERT, Convert)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEDEVICES_RESET, ResetStatus)

# data import
from tuoen.agile.apis.data.mobilephone import Upload, Search, Convert, Update, ResetStatus

user_service.add(Upload, Search, Convert, Update, ResetStatus)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEPHONE_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEPHONE_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEPHONE_EDIT, Update)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEPHONE_CONVERT, Convert)
rule_register.register_api(data_import_rules.DEFAULT_MOBILEPHONE_RESET, ResetStatus)

from tuoen.agile.apis.equipment.register import Update

user_service.add(Update)
rule_register.register_api(service_item_rules.DEFAULT_SERVICEITEM_EDIT, Update)

from tuoen.agile.apis.staffalias import Add, Search, Update, Remove

user_service.add(Add, Search, Update, Remove)
rule_register.register_api(staff_rules.DEFAULT_STAFFALIAS_QUERY, Search)
rule_register.register_api(staff_rules.DEFAULT_STAFFALIAS_EDIT, Update)
rule_register.register_api(staff_rules.DEFAULT_STAFFALIAS_ADD, Add)
rule_register.register_api(staff_rules.DEFAULT_STAFFALIAS_DEL, Remove)

from tuoen.agile.apis.product.product import Add, Search, Update, Remove

user_service.add(Add, Search, Update, Remove)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_QUERY, Search)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_EDIT, Update)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_ADD, Add)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_DEL, Remove)

from tuoen.agile.apis.product.productmodel import Add, Search, Update, Remove

user_service.add(Add, Search, Update, Remove)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_MODELQUERY, Search)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_MODELEDIT, Update)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_MODELADD, Add)
rule_register.register_api(product_rules.DEFAULT_PRODUCT_MODELDEL, Remove)

from tuoen.agile.apis.service.quality import Search

user_service.add(Search)
rule_register.register_api(service_item_rules.DEFAULT_QUALITY_QUERY, Search)
# demo
from tuoen.agile.apis.test.demo import Test, Filter

user_service.add(Test, Filter)

# data import
from tuoen.agile.apis.data.returns import Upload, Search, Convert, ResetStatus

user_service.add(Upload, Search, Convert, ResetStatus)
rule_register.register_api(data_import_rules.DEFAULT_RETURNS_QUERY, Search)
rule_register.register_api(data_import_rules.DEFAULT_RETURNS_UPLOAD, Upload)
rule_register.register_api(data_import_rules.DEFAULT_RETURNS_CONVERT, Convert)
rule_register.register_api(data_import_rules.DEFAULT_RETURNS_RESET, ResetStatus)

from tuoen.agile.apis.order.returns import Search, Get, Update, Remove, Change, Recover, Add

user_service.add(Get, Search, Update, Remove, Change, Recover, Add)
rule_register.register_api(order_rules.DEFAULT_ORDERRETURNS_REMOVE, Remove)
rule_register.register_api(order_rules.DEFAULT_ORDERRETURNS_QUERY, Search)
rule_register.register_api(order_rules.DEFAULT_ORDERRETURNS_ADD, Add)
rule_register.register_api(order_rules.DEFAULT_ORDERRETURNS_RECOVER, Recover)

from tuoen.agile.apis.customer.register import Search

user_service.add(Add, Search, Update)
rule_register.register_api(customer_rules.DEFAULT_CUSREGISTER_QUERY, Search)

from tuoen.agile.apis.customer.rebate import Search

user_service.add(Search)
rule_register.register_api(customer_rules.DEFAULT_CUSTOMERREBATE_QUERY, Search)

from tuoen.agile.apis.customer.transaction import Search

user_service.add(Search)
rule_register.register_api(customer_rules.DEFAULT_CUSTOMERTRANSACTION_QUERY, Search)

from tuoen.agile.apis.equipment.equipmentin import Search, Update

user_service.add(Search, Update)
rule_register.register_api(product_rules.DEFAULT_EQUIPMENTIN_QUERY, Search)
rule_register.register_api(product_rules.DEFAULT_EQUIPMENTIN_EDIT, Update)

from tuoen.agile.apis.equipment.equipmentout import Search, Update

user_service.add(Search, Update)
rule_register.register_api(product_rules.DEFAULT_EQUIPMENTOUT_QUERY, Search)
rule_register.register_api(product_rules.DEFAULT_EQUIPMENTOUT_EDIT, Update)

from tuoen.agile.apis.mobile.wechatphone import Search, Add, RemoveAll, Update

user_service.add(Search, Add, RemoveAll, Update)
rule_register.register_api(mobile_rules.DEFAULT_WECHAT_QUERY, Search)
rule_register.register_api(mobile_rules.DEFAULT_WECHAT_EDIT, Update)
rule_register.register_api(mobile_rules.DEFAULT_WECHAT_DEL, RemoveAll)
rule_register.register_api(mobile_rules.DEFAULT_WECHAT_ADD, Add)

from tuoen.agile.apis.permise.staff.departmentchange import Add, Search, Get, Update, Remove, Executed

user_service.add(Add, Search, Get, Update, Remove, Executed)
rule_register.register_api(staff_rules.DEFAULT_DEPARTMENTCHANGE_QUERY, Search)
rule_register.register_api(staff_rules.DEFAULT_DEPARTMENTCHANGE_EDIT, Get, Update)
rule_register.register_api(staff_rules.DEFAULT_DEPARTMENTCHANGE_ADD, Add)
rule_register.register_api(staff_rules.DEFAULT_DEPARTMENTCHANGE_DEL, Remove)
rule_register.register_api(staff_rules.DEFAULT_DEPARTMENTCHANGE_EXECUTED, Executed)

from tuoen.agile.apis.service.deptdev import Statistics, Search, Get

user_service.add(Search, Statistics, Get, EditSn)
rule_register.register_api(service_item_rules.DEFAULT_DEPTDEV_QUERY, Search, Statistics)
rule_register.register_api(service_item_rules.DEFAULT_DEPTDEV_EDIT, Get)

from tuoen.agile.apis.order.replenishment import Search, Remove, Export

user_service.add(Search, Remove, Export)
rule_register.register_api(order_rules.DEFAULT_ORDERREPLENISHMENT_QUERY, Search)
rule_register.register_api(order_rules.DEFAULT_ORDERREPLENISHMENT_DELETE, Remove)
rule_register.register_api(order_rules.DEFAULT_ORDERREPLENISHMENT_EXPORT, Export)

from tuoen.agile.apis.merchant import Add

user_service.add(Add)

from tuoen.agile.apis.merchant.transaction import Add

user_service.add(Add)

from tuoen.agile.apis.measure.statistics import Search, Statistics, ExportData

user_service.add(Search, Statistics, ExportData)
rule_register.register_api(measure_rules.DEFAULT_PERFORMANCE_QUERY, Search, Statistics)
rule_register.register_api(measure_rules.DEFAULT_PERFORMANCE_EXPORT, ExportData)

