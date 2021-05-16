# coding=utf-8
import os
from fabric.api import local, lcd, run, cd, task, sudo
from fabric.context_managers import env


def install_tools(pkgs):
    run("apt-get install %s" % pkgs)


def compile(url, pkg, ver):
    pkg_name = "%s-%s" % (pkg, ver)
    with cd("/data/tmp"):
        run("wget %s%s.tar.gz" % (url, pkg_name))
        run("tar -zxvf %s.tar.gz" % (pkg_name))

    with cd("/data/tmp/%s" % pkg_name):
        run("./configure")
        run("make && make install")


def install_nginx():
    compile("ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/", "pcre", "8.36")
    compile("http://nginx.org/download/", "nginx", "1.6.3")


def pip_install():
    with cd("/data/ebus/ebus/"):
        run("pip install -r requirements.txt -i %s" % "http://pypi.douban.com/simple/")


def clone_code():
    with cd("/data/ebus/"):
        git_url = "ebus@121.199.162.43:/git/ebus"
        run("git clone %s" % git_url)


def ensure_dir(dir):
    run("[ ! -d %s ] && mkdir %s " % (dir, dir))


def ensure_dirs():
    path_list = ["/data/ebus/", "/data/tmp"]
    for path in path_list:
        ensure_dir(path)


def set_env():
    with cd("/data/ebus/ebus"):
        run("fab genr_cfg")  # 生成配置文件
        run("fab mkdirs")  # 生成对应目录
        run("fab static")  # 迁移静态文件


def do_start():
    run("supervisord -c /etc/supervisord.conf")
    run("nginx -c /etc/nginx/nginx.conf")  # nginx放在默认的文件夹下
    # nginx有两个问题，第一个要建快捷方式，第二个是配置文件所在位置


def do_deploy():
    ensure_dirs()
    apt_get_list = ["git", "python-dev", "python-pip", "libmysqld-dev"]
    install_tools(' '.join(apt_get_list))
    install_nginx()
    clone_code()
    pip_install()
    python_lib_list = ["python-pycurl", "python-supervisor"]
    install_tools(' '.join(python_lib_list))  # TODO: 配置pillow？
    set_env()
    do_start()
