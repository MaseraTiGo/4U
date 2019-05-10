# coding=UTF-8

import init_envt

from tuoen.sys.utils.common.single import Single
from support.generator.helper import *
from support.init.loader import *


class InitManager(Single):

    def __init__(self):
        # staff init
        self._staff = StaffGenerator(StaffLoader().load())
        self._account = AccountGenerator()
        self._department = DepartmentGenerator(DepartmentLoader().load())
        self._role = RoleGenerator(RoleLoader().load())
        self._access = AuthAccessGenerator()

        # product init
        self._product = ProductGenerator(ProductLoader().load())
        self._product_model = ProductModelGenerator(ProductModelLoader().load())
        self._channel = ChannelGenerator(ChannelLoader().load())  # fsy
        self._shop = ShopGenerator(ShopLoader().load())
        self._goods = GoodsGenerator(GoodsLoader().load())

        self._customer = CustomerGenerator(CustomerLoader().load())  # fsy

    def generate_product_relate(self):
        self._shop.add_inputs(self._channel)
        self._product_model.add_inputs(self._product)
        self._goods.add_inputs(self._shop, self._product_model)
        return self._product


    def generate_staff_relate(self):
        self._staff.add_outputs(self._account)
        self._access.add_inputs(self._staff, self._role, self._department)
        return self._staff

    def run(self):
        staff_generator = self.generate_staff_relate()
        staff_generator.generate()

        product_generator = self.generate_product_relate()
        product_generator .generate()

        self._customer.generate()  # fsy

if __name__ == "__main__":
    InitManager().run()
