# coding=UTF-8

import init_envt

from tuoen.sys.utils.common.single import Single
from support.simulate.test.staff import StaffMaker
from support.simulate.test.product import ProductMaker
from support.simulate.test.storage import StorageMaker
from support.simulate.test.mobiledevices import MobileDevicesMaker
from support.simulate.test.customer import CustomerMaker


class TestDataManager(Single):

    def run(self):
        # generate staff
         StaffMaker().run(10)

        # generate product
         ProductMaker().run(1)

        # generate storage
         StorageMaker().run(1000)

        # generate mobilephone
         MobileDevicesMaker().run(10)

        # generate customer by staff
         CustomerMaker().run(10)


if __name__ == "__main__":
    TestDataManager().run()
