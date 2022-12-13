# -*- coding: utf-8 -*-
# @File    : executioner
# @Project : hitler_adolf
# @Time    : 2022/6/10 13:35
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import datetime
import json
import os

from nameko.events import EventDispatcher
from nameko.rpc import rpc

from logs import superDong
from settings import RECORD_CMD_SWITCH, MY_PREFIX
from utils.funcs import gen_today_log_path


class RemoteCmdExecutor:
    """ Event dispatching service. """
    name = "cmd"

    dispatch = EventDispatcher()

    @rpc
    def execute(self, instruction: dict):
        print(f"{MY_PREFIX} instruction: {instruction}")
        if RECORD_CMD_SWITCH:
            os.system(
                f'echo {str(datetime.datetime.today())}-instruction:{json.dumps(instruction)} >> '
                f'{gen_today_log_path()}'
            )
            # superDong.warning(f'instruction:\n {instruction}')
        self.dispatch('executor', instruction)
