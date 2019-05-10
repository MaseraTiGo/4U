# coding=utf-8
import os
from fabric.api import local, lcd, run, cd, task, sudo
from fabric.context_managers import env
from server import EbusWebServer


env.hosts = ['192.168.1.111', ]
env.user = 'root'
env.password = "yangrongkai"


def init_web():
    web = EbusWebServer()
    web.init_environment()

def init_web_config():
    web = EbusWebServer()
    web.configurate()