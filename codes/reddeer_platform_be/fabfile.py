# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: deploy_be
# DateTime: 2021/1/4 11:25
# Project: awesome_dong
# Do Not Touch Me!

import paramiko

import fabric
from invoke import Responder

# ------------------------------------- host env ----------------------------------------

HOSTNAME = '192.168.145.132'
USERNAME = 'dante'
PASSWORD = '123918'

SUDO_PATTERN = r'\[sudo\] password for dante:'
# ------------------------------------- host env ----------------------------------------


# ------------------------------------- git env ----------------------------------------
GIT_USERNAME_PATTERN = r'Username for'
GIT_PASSWORD_PATTERN = r'Password for'

GIT_USERNAME = 'dongjd'
GIT_PASSWORD = 'zxcvbnm123'

GIT_URL = 'http://192.168.3.251:10080/operating/reddeer_platform_be.git'

GIT_REPO = 'reddeer_platform_be'
GIT_VOLUME = 'red_deer_be'


# ------------------------------------- git env ----------------------------------------


class DanteDeploy:

    def __init__(self):
        self.con = fabric.Connection(f'{USERNAME}@{HOSTNAME}', connect_kwargs={'password': PASSWORD})

    def run(self, cmd, sudo=False, watcher=None):
        watchers = []
        sudo_watcher = Responder(pattern=SUDO_PATTERN, response='%s\n' % PASSWORD)
        watchers.append(sudo_watcher)
        if not sudo:
            if watcher:
                if isinstance(watcher, list):
                    watchers.extend(watcher)
                else:
                    watchers.append(watcher)
            return self.con.run(cmd, watchers=watchers).stdout.strip()
        else:
            if isinstance(watcher, list):
                watchers.extend(watcher)
            else:
                watchers.append(watcher)
            return self.con.run('sudo ' + cmd, pty=True, watchers=watchers).stdout.strip()


class DockerOperate:
    def __init__(self, con):
        self._con = con

    def check_and_install(self):
        cmd = 'sudo docker -v'
        if 'Docker version ' in self._con.run(cmd, sudo=True):
            ...
        else:
            ...

    @classmethod
    def create_volume(cls, name):
        ...

    @classmethod
    def exec_cmd(cls, cmd, con):
        ...


class GitOperate:
    ...


OS_RELEASE = ['ubuntu', 'red hat', 'centos']


def get_os_release():
    cmd = 'cat /proc/version'
    result = dante.run(cmd, sudo=True)
    for release in OS_RELEASE:
        if release in result.lower():
            return release
    raise Exception('can not get the release type of current os!')


def is_existed_docker():
    cmd = 'docker -v'
    result = dante.run(cmd, sudo=True)
    if 'Docker version' not in result:
        print('docker is not installed, now start to install docker')


def is_existed_git():
    ...


def is_existed_docker_compose():
    ...


def pull_source_codes():
    cmd = 'git clone '
    f_cmd = cmd + GIT_URL
    username_watcher = Responder(pattern=GIT_USERNAME_PATTERN, response='%s\n' % GIT_USERNAME)
    password_watcher = Responder(pattern=GIT_PASSWORD_PATTERN, response='%s\n' % GIT_PASSWORD)
    res = dante.run(f_cmd, sudo=True, watcher=[username_watcher, password_watcher])


def create_py_codes_volume():
    cmd = f'docker volume create {GIT_VOLUME}'
    dante.run(cmd, sudo=True)


def move_codes_2_dest():
    cmd = f'mv ~/{GIT_REPO}/* /var/lib/docker/volumes/{GIT_VOLUME}/'
    dante.run(cmd, sudo=True)


def pull_python_img():
    ...


def initial_db():
    ...


def backup_db():
    ...


def exec_docker_compose():
    pre_cmd = f'docker-composer -f ~/{GIT_REPO}/deploy/application/'
    web = 'web/docker-compose.yml up -d'
    nginx = 'balance/nginx/docker-compose.yml up -d'
    redis = 'cache/docker-compose.yml up -d'
    mysql = 'database/mysql/docker-compose.yml up -d'

    dante.run(pre_cmd + mysql)
    dante.run(pre_cmd + redis)
    dante.run(pre_cmd + nginx)
    dante.run(pre_cmd + web)


dante = DanteDeploy()

pull_source_codes()
create_py_codes_volume()
move_codes_2_dest()

temp = {"form_data": [{"id": 208, "name": "新的表单AAAAABBCCCC", "collections": [
    {"tag": 0, "list": [], "name": "开开心心", "type": 1, "value": "dqe32q", "checklist": []},
    {"tag": 2, "list": [], "name": "年龄", "type": 1, "value": "12", "checklist": []}, {"tag": 5,
                                                                                      "list": [{"label": "选项111"},
                                                                                               {"label": "选项2222"},
                                                                                               {"label": "选项3333"},
                                                                                               {"label": "选项4444"},
                                                                                               {"label": "选项5555"}],
                                                                                      "name": "单选", "type": 2,
                                                                                      "value": "2", "checklist": []},
    {"tag": 6, "list": [], "name": "所在地", "type": 3, "value": "辽宁省沈阳市和平区12321", "checklist": []},
    {"tag": 7, "list": [{"label": "选项1"}, {"label": "选项2"}, {"label": "选项3"}, {"label": "选项4"}, {"label": "选项5"}],
     "name": "多选", "type": 4, "value": "1,2,3", "checklist": ["1", "2", "3"]}]}]}
