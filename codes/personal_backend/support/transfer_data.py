# coding=UTF-8
import threading
import time
import init_envt

from support.transfer.channel import ChannelTransfer
from support.transfer.shop import ShopTransfer
from support.transfer.measureshop import MeasureShopTransfer
from support.transfer.equipmentin import EquipmentinTransfer
from support.transfer.equipmentout import EquipmentoutTransfer
from support.transfer.measurestaff import MeasureStaffTransfer
from support.transfer.mobiledevices import MobileDevicesTransfer
from support.transfer.mobilemaintain import MobileMaintainTransfer
from support.transfer.equipment import EquipmentTransfer
from support.transfer.equipmentrebate import EquipmentRebateTransfer
from support.transfer.equipmenttransaction import EquipmentTransactionTransfer
from support.transfer.equipmentregister import EquipmentRegisterTransfer
from support.transfer.modifystatus import ModifystatusTransfer
from support.transfer.order import OrderTransfer


class TransferDataManager():

    def run(self):
        '''
        ChannelTransfer().run()

        ShopTransfer().run()
        
        MeasureShopTransfer().run()

        EquipmentinTransfer().run()
        
        EquipmentoutTransfer().run()
 
        MeasureStaffTransfer().run()
     
        MobileDevicesTransfer().run()
        
        MobileMaintainTransfer().run()

        EquipmentRegisterTransfer().run()
        
        EquipmentRebateTransfer().run()
        
        EquipmentTransactionTransfer().run()
        
        EquipmentTransfer().run()
        
        ModifystatusTransfer().run()
        '''
        OrderTransfer().run()

if __name__ == "__main__":
    TransferDataManager().run()
