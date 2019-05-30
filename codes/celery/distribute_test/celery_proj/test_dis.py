# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '5/30/2019 9:32 AM'

import time
from tasks import add, multi

for _ in range(30):
    time.sleep(0.5)
    add.delay(3, 3)
    multi.delay(4, 4)
