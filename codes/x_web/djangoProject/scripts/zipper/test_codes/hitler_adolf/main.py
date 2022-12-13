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

import eventlet
from nameko.cli.run import import_service
from nameko.cli.run import run

from settings import AMQP_URI_CONF
from settings import LISTENERS
from settings import MY_PREFIX
from settings import SERVICES

eventlet.monkey_patch()


def _load_listener(listener: str) -> list:
    return import_service(f'listeners.{listener}')


def _load_service(service: str) -> list:
    return import_service(f'services.{service}')


if __name__ == '__main__':
    services = []

    services.extend([item for lis in LISTENERS for item in _load_listener(lis)])
    services.extend([item for ser in SERVICES for item in _load_service(ser)])
    print(f"{MY_PREFIX} services:\n{[item.name for item in services]}")
    print(f"{MY_PREFIX} ready to get ur instructions...")
    run(services, AMQP_URI_CONF)
