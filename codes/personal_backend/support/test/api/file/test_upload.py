# coding=UTF-8

import os
import json

from support.common.testcase.api_test_case import APITestCase
'''
class RegisterUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_register_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, '立佰趣客户查询.xlsx')
        files = {'立佰趣客户查询.xlsx': open(file_path, 'rb')}
        api = "data.register.upload"
        result = self.access_file_api(api, files = files, store_type = "test", flag = "user")

class RebateUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rebate_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, '立佰趣点刷实时返现.xlsx')
        files = {'立佰趣点刷实时返现.xlsx': open(file_path, 'rb')}
        api = "data.rebate.upload"
        result = self.access_file_api(api, files = files, store_type = "test", flag = "user")

class TransactionUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_transaction_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, '融密点刷交易流水20180516-20180516.xlsx')
        files = {'融密点刷交易流水20180516-20180516.xlsx': open(file_path, 'rb')}
        api = "data.transaction.upload"
        result = self.access_file_api(api, files = files, store_type = "test", flag = "user")

class BuyinfoUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_buyinfo_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, '管家婆05.14-05.17.xls')
        files = {'管家婆05.14-05.17.xls': open(file_path, 'rb')}
        api = "data.buyinfo.upload"
        result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        print(result)

class RegisterSearch(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_register_search(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.register.search"
        current_page = 1
        search_info = json.dumps({
            "code":"A007001416",
            "device_code":"730300011768100"
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class RebateSearch(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_register_search(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.rebate.search"
        current_page = 1
        search_info = json.dumps({
            "code":"A006644077",
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class TransactionSearch(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_transaction_search(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.transaction.search"
        current_page = 1
        search_info = json.dumps({
            "code":"A007400186"
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class BuyinfoSearch(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_buyinfo_search(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.buyinfo.search"
        current_page = 1
        search_info = json.dumps({
            "device_code":"F323850300010471967"
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class BuyinfoConvert(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_buyinfo_convert(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.buyinfo.convert"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)

class BuyinfoUpdate(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_buyinfo_update(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.buyinfo.update"
        buyinfo_id = 21
        buyinfo_info = json.dumps({
            "remark": "kf丁玲kf wx8064wx bz55+3 刷满3000返红包 返购机款22bz",
            "device_code": "850300010471988"
        })

        result = self.access_api(flag = flag, api = api, buyinfo_id = buyinfo_id, buyinfo_info = buyinfo_info)

class RegisterConvert(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_register_convert(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.register.convert"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)

class TransactionConvert(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_transaction_convert(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.transaction.convert"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)

class RebateConvert(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rebate_convert(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.rebate.convert"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)

class EquipmentInUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equipment_in_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, '点刷进货号段.xlsx')
        files = {'点刷进货号段.xlsx': open(file_path, 'rb')}
        api = "data.equipmentin.upload"
        result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        print(result["error_list"])

class EquipmentInSearch(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equipment_in_search(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.equipmentin.search"
        current_page = 1
        search_info = json.dumps({
             'add_time':"2018-05-15",
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class EquipmentInConvert(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equipment_in_convert(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.equipmentin.convert"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)

class EquipmentInUpdate(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equipment_in_update(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.equipmentin.update"
        equipment_in_id = 58
        equipment_in_info = json.dumps({
            "min_number": "410300010367911",
            "max_number": "410300010368010"
        })

        result = self.access_api(flag = flag, api = api, equipment_in_id = equipment_in_id, \
                                 equipment_in_info = equipment_in_info)

class EquipmentOutUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equipment_out_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, '点刷出库号段.xlsx')
        files = {'点刷出库号段.xlsx': open(file_path, 'rb')}
        api = "data.equipmentout.upload"
        result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        print(result["error_list"])

class EquipmentOutSearch(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equipment_out_search(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.equipmentout.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class EquipmentOutConvert(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equipment_out_convert(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.equipmentout.convert"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)

class EquipmentOutUpdate(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equipment_out_update(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.equipmentout.update"
        equipment_out_id = 2495
        equipment_out_info = json.dumps({
            "min_number": "720300010029182",
            "max_number": "720300010029231"
        })

        result = self.access_api(flag = flag, api = api, equipment_out_id = equipment_out_id, \
                                 equipment_out_info = equipment_out_info)


class StaffUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, '必圈员工通讯录(41)修改.xlsx')
        files = {'必圈员工通讯录(41)修改.xlsx': open(file_path, 'rb')}
        api = "data.staff.upload"
        result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        print(result["error_list"])

class StaffSearch(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_search(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.staff.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])


class StaffUpdate(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_update(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.staff.update"
        staff_id = 1
        staff_info = json.dumps({
            "age": 24,
        })

        result = self.access_api(flag = flag, api = api, staff_id = staff_id, \
                                 staff_info = staff_info)


class StaffConvert(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_convert(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.staff.convert"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)


class MobileDevicesUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_devices_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, '微信手机盘点.xlsx')
        files = {'微信手机盘点.xlsx': open(file_path, 'rb')}
        api = "data.mobiledevices.upload"
        result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        print(result["error_list"])
'''

class MobileDevicesSearch(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_devices_search(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.mobiledevices.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        print(result["data_list"])
'''

class MobileDevicesUpdate(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_phone_update(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.mobiledevices.update"
        mobile_devices_id = 1
        mobile_devices_info = json.dumps({
            "wechat_nick": "三色石1111",
        })

        result = self.access_api(flag = flag, api = api, mobile_devices_id = mobile_devices_id, \
                                 mobile_devices_info = mobile_devices_info)

class MobilePhoneUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_phone_upload_file(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, '手机号信息.xlsx')
        files = {'手机号信息.xlsx': open(file_path, 'rb')}
        api = "data.mobilephone.upload"
        result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        print(result["error_list"])

class MobilePhoneSearch(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_phone_search(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.mobilephone.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class MobilePhoneUpdate(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_phone_update(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.mobilephone.update"
        mobile_phone_id = 1
        mobile_phone_info = json.dumps({
            "operator": "电信111",
        })

        result = self.access_api(flag = flag, api = api, mobile_phone_id = mobile_phone_id, \
                                 mobile_phone_info = mobile_phone_info)

class MobilePhoneConvert(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_phone_convert(self):

        # result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        flag = "user"
        api = "data.mobilephone.convert"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)
'''
