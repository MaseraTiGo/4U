# coding=UTF-8

import os
import string
import multiprocessing

from fabric.api import local, lcd, run, cd, task, sudo
from fabric.context_managers import env, settings

from base_oper import *

PROJECT_STORE = '/data'
PROJECT_STORE_TEMP = PROJECT_STORE + "/temp"

EBUS_WORK_ROOT = PROJECT_STORE + "/ebus"
EBUS_PROJECT_ROOT = EBUS_WORK_ROOT + "/ebus"
EBUS_DEPLOY_ROOT = EBUS_PROJECT_ROOT + "/deploy"
EBUS_DEPLOY_TEMPLATE = EBUS_DEPLOY_ROOT + "/conf"
EBUS_LOG_ROOT = EBUS_WORK_ROOT + "/log"
EBUS_TOOL_CONF_ROOT = EBUS_WORK_ROOT + "/conf"


class CfgTemplate(object):

    def __init__(self, tmpl_file, dest_file, variables):
        self.tmpl_file = tmpl_file
        self.dest_file = dest_file
        self.variables = variables

    def load_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return content
        except Exception as e:
            print("load_file error, path=%s, e=%s" % (file_path, e))
            return ''

    def save_file(self, file_path, content):
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print("save_cfg error, path=%s, e=%s" % (file_path, e))
            return False

    def __call__(self):
        template = self.load_file(self.tmpl_file)
        if not template:
            raise Exception("org_file does not exist or is empty, path=%s" % self.tmpl_file)

        te = string.Template(template)
        content = te.safe_substitute(self.variables)
        result = self.save_file(self.dest_file, content)

        if not result:
            raise Exception("dest_file save error, check is path exists: %s" % self.dest_file)
        print
        "genrate config file OK, dest_path=%s" % self.dest_file


class BaseServer(object):

    def init_environment(self):
        raise NotImplementedError("server need to implement init_environment function")

    def stop(self):
        raise NotImplementedError("server need to implement stop function")

    def start(self):
        raise NotImplementedError("server need to implement start function")

    def restart(self):
        raise NotImplementedError("server need to implement restart function")


class WebServer(BaseServer):

    def __init__(self):
        self.project_store = PROJECT_STORE
        self.temp_dir = PROJECT_STORE_TEMP

    def _apt_get(self):
        run('apt-get update')
        return [
            'git',
            'python-dev',
            'python-pip',
            'libmysqlclient-dev',
            'libmysqld-dev',
            "python-pycurl",
            "supervisor",

            "libxml2",
            "libxml2-dev",
            "libxslt1.1",
            "libxslt1-dev",

            "libjpeg-dev",
            "libfreetype6-dev",

            "zlib1g",
            "zlib1g.dev",
            "libpcre3",
            "libpcre3-dev",
            'gcc',
            'build-essential'
        ]

    def _pip_list(self):
        return [
            "gevent==1.0.1",
            "gunicorn==19.3.0",
        ]

    def install_nginx(self):
        #         compile("ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/", self.temp_dir, "pcre-8.36")
        #         compile("http://nginx.org/download/", self.temp_dir, "nginx-1.6.3")
        compile("http://nginx.org/download/", self.temp_dir, "nginx-1.9.2")

    def deploy_project(self):
        return True

    def init_environment(self):
        make_dir([self.project_store, self.temp_dir])
        apt_install(self._apt_get())
        pip_install(self._pip_list())
        self.install_nginx()
        self.deploy_project()


class EbusWebServer(WebServer):
    def __init__(self):
        super(EbusWebServer, self).__init__()
        self.work_dir = EBUS_WORK_ROOT
        self.conf_path = EBUS_DEPLOY_ROOT
        self.conf_template = EBUS_DEPLOY_TEMPLATE
        self.project_root = EBUS_PROJECT_ROOT
        self.project_conf = EBUS_TOOL_CONF_ROOT
        self.project_log = EBUS_LOG_ROOT

        self.project_name = "ebus"
        self.code_url = "ebus@121.199.162.43:/git/ebus"
        self.depend_file = "requirements.txt"
        self.download_path = self.project_root + "/site_media/upload"

        #         self.nginx_template = os.path.join(self.conf_template, 'nginx.conf')
        #         self.nginx_exec_file = os.path.join(self.project_conf, "nginx.conf")
        #         self.supervisord_template = os.path.join(self.conf_template, 'supervisord.conf')
        #         self.supervisord_exec_file = os.path.join(self.project_conf, "supervisord.conf")

        self.nginx_template = self.conf_template + '/nginx.conf'
        self.nginx_exec_file = self.project_conf + "/nginx.conf"
        self.supervisord_template = self.conf_template + '/supervisord.conf'
        self.supervisord_exec_file = self.project_conf + "/supervisord.conf"

    def _base_args(self):
        def genr_core_list(cores):
            result_list = []
            template = cores * '0'
            for i in reversed(range(cores)):
                result_list.append("%s1%s" % (template[:i], template[i + 1:]))
            return ' '.join(result_list)

        cores = multiprocessing.cpu_count()
        workers = 2 * cores + 1
        core_list = genr_core_list(cores)

        variables = {'cores': cores,
                     'workers': workers,
                     'core_list': core_list,
                     'prj_path': self.project_root.replace('\\', '/'),
                     'log_path': self.project_log.replace('\\', '/'),
                     'con_num': 30000 / cores,
                     'prj_name': self.project_name}
        return variables

    def _configurate_nginx(self):
        variables = self._base_args()
        CfgTemplate(tmpl_file=self.nginx_template, dest_file=self.nginx_exec_file, variables=variables)()

    def _supervor_nginx(self):
        variables = self._base_args()
        CfgTemplate(tmpl_file=self.supervisord_template, dest_file=self.supervisord_exec_file, variables=variables)()

    def configurate(self):
        self._configurate_nginx()
        self._supervor_nginx()

    def run_configurate(self):
        with cd(self.conf_path):
            run("fab init_web_config")

    def init_app_struct(self):
        path_file = self.work_dir + "/" + self.project_name
        rm(path_file)
        work_others = [self.project_conf, self.project_log, self.project_root]
        make_dir(work_others)

    def init_project_struct(self):
        project_downloads = ['temp', 'group_img', 'stop_img', 'role_img']
        project_downloads = map(lambda x: '%s/%s' % (self.download_path, x), project_downloads)
        make_dir(project_downloads)

    def _depend_package(self):
        return ['Django==1.7.3',
                'Fabric==1.10.1',
                'MySQL-python==1.2.5',
                'pyquery==1.2.9',
                'python-memcached==1.53',
                'requests==2.5.1',
                'rsa==3.1.4',
                'Pillow==2.7.0',
                'xlrd==0.9.3',
                'PIL']

    def start_project(self):
        with settings(warn_only=True):
            run("nginx -s stop")
            run("nginx -c %s" % (self.nginx_exec_file))
            run("supervisorctl stop %s" % (self.project_name))
            run("supervisord -c %s" % (self.supervisord_exec_file))

    def deploy_project(self):
        self.init_app_struct()  # 0、初始化 app包结构
        clone_code(self.work_dir, self.code_url)  # 1、克隆代码
        self.init_project_struct()  # 2、初始化项目目录结构
        pip_install(self._depend_package())  # 3、初始化项目依赖包
        self.run_configurate()  # 4、配置架构配置文件
        self.start_project()  # 5、启动项目


class CacheServer(BaseServer):
    pass


class FileServer(BaseServer):
    pass


class TimerServer(BaseServer):
    pass


class DBServer(BaseServer):
    pass


if __name__ == "__main__":
    x = EbusWebServer()
    x.init_environment()
