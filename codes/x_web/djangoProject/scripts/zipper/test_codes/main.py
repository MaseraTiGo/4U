# -*- coding: utf-8 -*-
# @File    : main
# @Project : hitler_adolf
# @Time    : 2022/6/6 16:31
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import json
import os
import subprocess

from nameko.events import EventDispatcher
from nameko.events import event_handler, BROADCAST
from nameko.rpc import rpc

from settings import RECORD_CMD_SWITCH, MY_PREFIX
from utils.funcs import gen_today_log_path
from utils.host import host_name
from utils.redis_op import redis_trans_broker


class RemoteCmdExecutor:
    """ Event dispatching service. """
    name = "cmd"

    dispatch = EventDispatcher()

    @rpc
    def execute(self, instruction: dict):
        print(f"{MY_PREFIX} instruction: {instruction}")
        if RECORD_CMD_SWITCH:
            os.system(
                f'echo instruction:{json.dumps(instruction)} >> '
                f'{gen_today_log_path()}'
            )
        self.dispatch('executor', instruction)


class DenHaiSan:
    """
     Event listening service.
    """

    name = "listener"

    @event_handler(
        "cmd", "executor",
        handler_type=BROADCAST,
        reliable_delivery=False
    )
    def execute_cmd(self, instruction: dict):
        cmd_info = instruction['cmd_info']
        nodes = cmd_info.get('nodes')

        if host_name not in nodes:
            return

        cmd = cmd_info.get('cmd')
        print(f"{MY_PREFIX} exe cmd:\n{cmd}")
        if RECORD_CMD_SWITCH:
            os.system(f'echo {cmd} >> {gen_today_log_path()}')

        res = subprocess.run(
            cmd,
            shell=True,
            universal_newlines=True,
            timeout=7,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        res, err = res.stdout, res.stderr

        ans = {
            "result": res,
            "code": 0 if not err else 1
        }
        store_key = instruction['store_key']
        redis_trans_broker.set(f'{store_key}-{host_name}', ans)
        # if err:
        #     return {"result": res, "code": 1}
        # else:
        #     return {"result": res, "code": 0}
