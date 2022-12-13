# -*- coding: utf-8 -*-
# @File    : clean_sw
# @Project : icr_mw
# @Time    : 2022/6/29 15:07
"""
                                      /
 __.  , , , _  _   __ ______  _    __/  __ ____  _,
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /|
                                                |/
"""

import subprocess


def execute_cmd(cmd: str):
    res = subprocess.run(
        cmd,
        shell=True,
        universal_newlines=True,
        timeout=7,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,

    )

    res, err = res.stdout, res.stderr
    if not err:
        return [item for item in res.split('\n') if item]
    return err


def deal_with_default_br(sw):
    ports = execute_cmd(f'ovs-vsctl list-ports {sw}')
    for p in ports:
        if ('@' not in p) and ('tap' not in p):
            continue
        execute_cmd(f'ovs-vsctl del-port {sw} {p}')


def fuck_it():
    sws = execute_cmd('ovs-vsctl list-br')
    for sw in sws:
        if '@' in sw:
            execute_cmd(f'ovs-vsctl del-br {sw}')
        else:
            deal_with_default_br(sw)


if __name__ == '__main__':
    fuck_it()

