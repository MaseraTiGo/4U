# coding=UTF-8

import init_envt
import json
import time


from support.repair.equipment import EquipmentRepair
from support.repair.logistics import LogisticsRepair
from support.repair.order import OrderRepair
from support.repair.service import ServiceRepair
from support.repair.orderevent import OrderEventRepair
from support.repair.measurestaff import MeasureStaffRepair
from support.repair.orderitem import OrderItemRepair
from support.repair.logisticsitem import LogisticsItemRepair
from support.repair.register import RegisterRepair
from support.repair.number import NumberRepair
from support.transfer.order import OrderTransfer
from support.repair.orderitem.repair_price import OrderItemPriceRepair


class RepairEquipmentDataManager():

    def run(self):

        time_start = time.time()
        print("====开始时间====", time_start)
        '''
        EquipmentRepair().run()
             
        ServiceRepair().run()
            
        OrderEventRepair().run()
        
        MeasureStaffRepair().run()
        
        
        OrderItemRepair().run()

        LogisticsRepair().run()

        LogisticsItemRepair().run()

        NumberRepair().run()
        
        OrderTransfer().run()
        '''
        OrderItemPriceRepair().run()

        OrderRepair().run()
        '''
        RegisterRepair().run()
        '''

        time_end = time.time()

        print("====结束时间====", time_end)
        print("====相差时间====", time_end - time_start)

if __name__ == "__main__":
    RepairEquipmentDataManager().run()
