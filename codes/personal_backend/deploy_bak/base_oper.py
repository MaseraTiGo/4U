# coding=UTF-8

from fabric.api import local, lcd, run, cd, task, sudo
from fabric.context_managers import env, settings

def clone_code(root_path, code_url):
    with cd(root_path):
        run("git clone %s" % code_url)

def make_dir(dirs):
    with settings(warn_only = True):
        for dir in dirs:
            run("mkdir -p %s " % (dir))

def rm(file_path):
    with settings(warn_only = True):
        run("rm -rf %s " % (file_path))

def apt_install(pkgs):
    with settings(warn_only = True):
        for pkg in pkgs:
            run("apt-get -y install %s" % pkg)

def compile(url, temp_dir, pkg_name):
    with cd(temp_dir):
        run("wget %s%s.tar.gz" % (url, pkg_name))
        run("tar -zxvf %s.tar.gz" % (pkg_name))

    with cd("%s/%s" % (temp_dir, pkg_name)):
        run("./configure")
        run("make && make install")

def pip_install(pip_list):
    with settings(warn_only = True):
        for pip in pip_list:
            run("pip install %s" % (pip))

def pip_install_byfile(dir_path, file_name):
    with cd(dir_path):
#         run("pip install -r %s -i %s" % ('%s/%s' % (dir_path, file_name), "http://pypi.douban.com/simple/"))
        run("pip install -r %s " % '%s/%s' % (dir_path, file_name))