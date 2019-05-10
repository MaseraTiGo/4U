# coding=UTF-8

import time
from tuoen.sys.utils.common.single import Single
from tuoen.abs.middleware.data.register import RegisterImport
from tuoen.abs.middleware.data.rebate import RebateImport
from tuoen.abs.middleware.data.transaction import TransactionImport
from tuoen.abs.middleware.data.buyinfo import BuyinfoImport
from tuoen.abs.middleware.data.equipmentin import EquipmentInImport
from tuoen.abs.middleware.data.equipmentout import EquipmentOutImport
from tuoen.abs.middleware.data.importstaff import StaffImport
from tuoen.abs.middleware.data.importmobiledevices import MobileDevicesImport
from tuoen.abs.middleware.data.importmobilephone import MobilephoneImport
from tuoen.abs.middleware.data.importreturns import ReturnsImport


class ImportRegisterMiddleware(Single):

    def import_register(self, f):
        register_list, error_list = RegisterImport().run(f)
        return register_list, error_list

    def exec_register(self, **search):
        success_list, failed_list = RegisterImport().convert(**search)
        return success_list, failed_list

    def run_register(self, f):
        pass

    def search(self, current_page, **search_info):
        return RegisterImport().search(current_page, **search_info)

    def reset_status(self, **search_info):
        RegisterImport().reset_status(**search_info)

import_register_middleware = ImportRegisterMiddleware()


class ImportRebateMiddleware(Single):

    def import_rebate(self, f):
        rebate_list, error_list = RebateImport().run(f)
        return rebate_list, error_list

    def exec_rebate(self, **search):
        success_list, failed_list = RebateImport().convert(**search)
        return success_list, failed_list

    def run_rebate(self, f):
        pass

    def search(self, current_page, **search_info):
        return RebateImport().search(current_page, **search_info)

    def reset_status(self, **search_info):
        RebateImport().reset_status(**search_info)

import_rebate_middleware = ImportRebateMiddleware()


class ImportTransactionMiddleware(Single):

    def import_transaction(self, f):
        transaction_list, error_list = TransactionImport().run(f)
        return transaction_list, error_list

    def exec_transaction(self, **search):
        success_list, failed_list = TransactionImport().convert(**search)
        return success_list, failed_list

    def run_transaction(self, f):
        pass

    def search(self, current_page, **search_info):
        return TransactionImport().search(current_page, **search_info)

    def reset_status(self, **search_info):
        TransactionImport().reset_status(**search_info)

import_transaction_middleware = ImportTransactionMiddleware()


class ImportBuyinfoMiddleware(Single):

    def import_buyinfo(self, f):
        buyinfo_list, error_list = BuyinfoImport().run(f)
        return buyinfo_list, error_list

    def exec_buyinfo(self, **search):
        success_list, failed_list = BuyinfoImport().convert(**search)
        return success_list, failed_list

    def run_buyinfo(self, f):
        pass

    def search(self, current_page, **search_info):
        return BuyinfoImport().search(current_page, **search_info)

    def update(self, buyinfo_id, **attr):
        import_customer_buyinfo = BuyinfoImport().get_object_byid(buyinfo_id)
        attr.update({"status":"init", "error_text":""})
        return BuyinfoImport().update_object(import_customer_buyinfo, **attr)

    def remove(self, buyinfo):
        BuyinfoImport().remove(buyinfo)

    def reset_status(self, **search_info):
        BuyinfoImport().reset_status(**search_info)

import_buyinfo_middleware = ImportBuyinfoMiddleware()


class ImportEquipmentInMiddleware(Single):

    def import_equipment_in(self, f):
        equipment_in_list, error_list = EquipmentInImport().run(f)
        return equipment_in_list, error_list

    def exec_equipment_in(self, **search):
        success_list, failed_list = EquipmentInImport().convert(**search)
        return success_list, failed_list

    def run_equipment_in(self, f):
        pass

    def search(self, current_page, **search_info):
        print("=====================================>>>>> ", search_info)
        return EquipmentInImport().search(current_page, **search_info)

    def update(self, equipment_in_id, **attr):
        import_equipment_in = EquipmentInImport().get_object_byid(equipment_in_id)
        attr.update({"status":"init", "error_text":""})
        return EquipmentInImport().update_object(import_equipment_in, **attr)

    def reset_status(self, **search_info):
        EquipmentInImport().reset_status(**search_info)

import_equipment_in_middleware = ImportEquipmentInMiddleware()


class EquipmentOutImportMiddleware(Single):

    def import_equipment_out(self, f):
        equipment_out_list, error_list = EquipmentOutImport().run(f)
        return equipment_out_list, error_list

    def exec_equipment_out(self, **search):
        success_list, failed_list = EquipmentOutImport().convert(**search)
        return success_list, failed_list

    def run_equipment_out(self, f):
        pass

    def search(self, current_page, **search_info):
        return EquipmentOutImport().search(current_page, **search_info)

    def update(self, equipment_out_id, **attr):
        import_equipment_out = EquipmentOutImport().get_object_byid(equipment_out_id)
        attr.update({"status":"init", "error_text":""})
        return EquipmentOutImport().update_object(import_equipment_out, **attr)

    def reset_status(self, **search_info):
        EquipmentOutImport().reset_status(**search_info)

import_equipment_out_middleware = EquipmentOutImportMiddleware()


class StaffImportMiddleware(Single):

    def import_staff(self, f):
        staff_list, error_list = StaffImport().run(f)
        return staff_list, error_list

    def exec_staff(self, **search):
        success_list, failed_list = StaffImport().convert(**search)
        return success_list, failed_list

    def run_staff(self, f):
        pass

    def search(self, current_page, **search_info):
        return StaffImport().search(current_page, **search_info)

    def update(self, staff_id, **attr):
        import_staff = StaffImport().get_object_byid(staff_id)
        attr.update({"status":"init", "error_text":""})
        return StaffImport().update_object(import_staff, **attr)

    def reset_status(self, **search_info):
        StaffImport().reset_status(**search_info)

import_staff_middleware = StaffImportMiddleware()


class MobileDevicesImportMiddleware(Single):

    def import_mobile_devices(self, f):
        mobile_devices_list, error_list = MobileDevicesImport().run(f)
        return mobile_devices_list, error_list

    def exec_mobile_devices(self, **search):
        success_list, failed_list = MobileDevicesImport().convert(**search)
        return success_list, failed_list

    def run_mobile_devices(self, f):
        pass

    def search(self, current_page, **search_info):
        return MobileDevicesImport().search(current_page, **search_info)

    def update(self, mobile_devices_id, **attr):
        import_mobile_devices = MobileDevicesImport().get_object_byid(mobile_devices_id)
        attr.update({"status":"init", "error_text":""})
        return MobileDevicesImport().update_object(import_mobile_devices, **attr)

    def reset_status(self, **search_info):
        MobileDevicesImport().reset_status(**search_info)

import_mobile_devices_middleware = MobileDevicesImportMiddleware()


class MobilePhoneImportMiddleware(Single):

    def import_mobile_phone(self, f):
        mobile_phone_list, error_list = MobilephoneImport().run(f)
        return mobile_phone_list, error_list

    def exec_mobile_phone(self, **search):
        success_list, failed_list = MobilephoneImport().convert(**search)
        return success_list, failed_list

    def run_mobile_phone(self, f):
        pass

    def search(self, current_page, **search_info):
        return MobilephoneImport().search(current_page, **search_info)

    def update(self, mobile_phone_id, **attr):
        import_mobile_phone = MobilephoneImport().get_object_byid(mobile_phone_id)
        attr.update({"status":"init", "error_text":""})
        return MobilephoneImport().update_object(import_mobile_phone, **attr)

    def reset_status(self, **search_info):
        MobilephoneImport().reset_status(**search_info)

import_mobile_phone_middleware = MobilePhoneImportMiddleware()

class ReturnsImportMiddleware(Single):

    def import_returns(self, f):
        returns_list, error_list = ReturnsImport().run(f)
        return returns_list, error_list

    def exec_returns(self, **search):
        success_list, failed_list = ReturnsImport().convert(**search)
        return success_list, failed_list

    def run_returns(self, f):
        pass

    def search(self, current_page, **search_info):
        return ReturnsImport().search(current_page, **search_info)

    def update(self, code, **attr):
        import_returns_temp = ReturnsImport().get_object_byid(code)
        attr.update({"status":"init", "error_text":""})
        return ReturnsImport().update_object(import_returns_temp, **attr)

    def reset_status(self, **search_info):
        ReturnsImport().reset_status(**search_info)

import_returns_middleware = ReturnsImportMiddleware()

