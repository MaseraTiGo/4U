# coding=UTF-8

# staff generator
from support.generator.helper.staff import StaffGenerator
from support.generator.helper.account import AccountGenerator
from support.generator.helper.department import DepartmentGenerator
from support.generator.helper.role import RoleGenerator
from support.generator.helper.authaccess import AuthAccessGenerator


# product generator
from support.generator.helper.product import ProductGenerator, ProductModelGenerator
from support.generator.helper.shop import ChannelGenerator, ShopGenerator, GoodsGenerator


# storage generator
from support.generator.helper.storage import EquipmentGenerator


# mobile phone generator
from support.generator.helper.mobiledevices import MobileDevicesGenerator, MobilePhoneGenerator, MobileMaintainGenerator


# customer generator
from support.generator.helper.customer import CustomerGenerator,\
        SaleChanceGenerator, OrderGenerator, OrderItemGenerator,\
        LogisticsGenerator, LogisticsItemGenerator, ServiceGenerator,\
        ServiceItemGenerator
