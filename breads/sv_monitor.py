#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2022/5/11 5:34 下午
import abc
import os
import pathlib
import subprocess
import sys
import time
import smtplib
import datetime
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback

from ruamel import yaml

try:
    import MySQLdb
except ImportError:
    import pymysql
    pymysql.install_as_MySQLdb()

LogFile = '/data/log/mw/sv_monitor.log'
FROMADDR = "whrd@cy-tech.net"
SMTPADDR = "smtp.mxhichina.com"  # 配置参考 https://help.aliyun.com/document_detail/36687.html
TOADDRS = [
    # "qiubao.xue@cy-tech.net",
    "ifw@cy-tech.net",
]
SUBJECT = "「chorplat」故障重启，请定位问题~"
PASSWORD = "CYkj@1102"
MSG = ""

SV_NGIFW = 'sv_ngifw'


Yaml_Path = "/usr/prj/config/mw/setting.yaml"

SYSLOG_ALARM = '/data/flags/send-log-flag'
EMAIL_ALARM = '/data/flags/send-email-flag'


class SysLog(object):
    """操作日志处理"""

    def __init__(self, log_name):
        """初始化log配置"""
        self.name = log_name
        self.host = "127.0.0.1"
        self.port = 50816

    def send(self, msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.sendto(msg.encode("utf-8"), (self.host, self.port))
        except Exception as ret:
            print(ret)
        s.close()

    def info(self, msg, level):
        """
        需要保存到数据库的字段：id, 时间, 用户, 操作内容（msg）, 操作结果
        :param msg: str-操作信息
        :return:
        """
        operate_fmt = '[IFW][SYS][{MODEL}][{LEVEL}]:CONTENT="{msg}"'.format(LEVEL=level, MODEL=self.name,
                                                                            msg=msg.replace(" ", ""))
        self.send(operate_fmt)

sysconfig_log = SysLog("SYSTEM")


def get_mgmt_ip():
    with open(Yaml_Path, 'r', encoding='utf-8') as hulk:
        try:
            yaml_data = yaml.load(hulk, Loader=yaml.RoundTripLoader)
        except Exception as e:
            return 'unknown'

        return yaml_data['ipset']['local']['localIp']

def execute_cmd(cmd):
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def error_detail(pid):

    def get_error_file(pid):
        for file in os.listdir('/data/coredump'):
            if f'-{pid}-' in file:
                return f'/data/coredump/{file}'
        return None

    error_file = get_error_file(pid)
    if not error_file:
        return 'unknown error'

    cmd = f'gdb -x /usr/prj/bin/getdump -c {error_file} /usr/prj/bin/chorplat'
    execute_cmd(cmd)
    time.sleep(10)

    if os.path.exists('/usr/prj/bin/gdb_bt.txt'):
        file = '/usr/prj/bin/gdb_bt.txt'
        with open(file, "r") as f:
            data = f.read()
        execute_cmd(f'rm {file}')
        return data
    return 'unknown error'

def add_log(s):
    with open(LogFile, 'a') as f:
        f.write(str(datetime.datetime.now()) + '----->' + s + '\n')

def sendmail(
        subject=SUBJECT,
        toaddrs=TOADDRS,
        fromaddr=FROMADDR,
        smtpaddr=SMTPADDR,
        password=PASSWORD,
        msg=None,
):
    """
    @subject:邮件主题
    @msg:邮件内容
    @toaddrs:收信人的邮箱地址
    @fromaddr:发信人的邮箱地址
    @smtpaddr:smtp服务地址
    @password:发信人的邮箱密码
    """

    mail_msg = MIMEMultipart()
    try:
        mgmt_ip = get_mgmt_ip()
    except:
        mgmt_ip = 'unknown'

    subj = f'ip:{mgmt_ip}--->' + subject + str(time.time())
    mail_msg['Subject'] = subj
    mail_msg['From'] = fromaddr
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg.attach(MIMEText(msg, 'plain', 'utf-8'))
    try:
        s = smtplib.SMTP_SSL(smtpaddr)
        s.connect(smtpaddr, 465)  # 连接smtp服务器
        s.login(fromaddr, password)  # 登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string())  # 发送邮件
        add_log('----send success-----')
        s.quit()
    except Exception as e:
        add_log('----send failed-----')
        add_log(str(traceback.format_exc()))

def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()


class DbOperator(object):

    def __init__(self,
                 db=None,
                 host='localhost', port=3306,
                 user='cyadmin', passwd='cykj1235'
                 ):
        self.db = db
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db_handler = None
        self.cursor = None

    def execute_and_fetchall(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def __enter__(self):
        self.db_handler = MySQLdb.connect(
            db=self.db,
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd
        )
        self.cursor = self.db_handler.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db_handler:
            self.db_handler.close()
        if any([exc_type, exc_val, exc_tb]):
            add_log(f"exc_type: {exc_type}|exc_val: {exc_val}|exc_tb: {exc_tb}")
            return True


class BaseFileParser(abc.ABC):

    def __init__(self, file_path, mode='r'):
        if not pathlib.Path(file_path).is_file():
            raise Exception(f"no such file!: {self._file_path}")
        self._file_path = file_path

        self._mode = mode

    @property
    @abc.abstractmethod
    def data(self):
        """must be implement in your subclass"""

    @abc.abstractmethod
    def write(self, data):
        """must be implement in your subclass"""


class YamlFileParser(BaseFileParser):

    @property
    def data(self):
        with open(self._file_path, self._mode, encoding='utf-8') as hulk:
            try:
                yaml_data = yaml.load(hulk, Loader=yaml.RoundTripLoader)
            except Exception as e:
                print(f"open file and read failed!: {self._file_path}"
                      f"exception: {e}")
                yaml_data = None
            return yaml_data

    def write(self, data, mode='w', version=None):
        ans = True
        with open(self._file_path, mode=mode, encoding='utf-8') as hulk:
            try:
                if version:
                    yaml.dump(data, allow_unicode=True, stream=hulk,
                              Dumper=yaml.RoundTripDumper,
                              version=version)
                else:
                    yaml.dump(data, allow_unicode=True, stream=hulk,
                              Dumper=yaml.RoundTripDumper)
            except Exception as e:
                ans = False
                print(f"write file failed!: {self._file_path}"
                      f"exception: {e}")
        return ans


class NetWorkManagerBase(object):
    EthYamlPath = "/usr/prj/config/hw/hw.yaml"

    SettingYamlPath = Yaml_Path

    Table = 'ng_ifw_eth_config'
    # if not settings.DEBUG:
    # @classmethod
    # def get_ports_name(cls):
    try:
        yaml_ins = YamlFileParser(EthYamlPath)
        net_data = yaml_ins.data["net"]
        link_pair = net_data["pair"]
        name_list = []
        pair_dict = {}  # 接口对
        bpslot_dict = {}
        b_pid_dict = {}
        bypass_cap_dict = {}
        bw = {}
        mtu_dict = {}
        mport_list = []
        addr_dict = {}
        for pair in link_pair:
            pair_spl = pair.split("-")
            pair_dict[pair_spl[0]] = pair_spl[1]
            pair_dict[pair_spl[1]] = pair_spl[0]
        for port in net_data.get("mport", {}).values():
            name = port["name"]
            mport_list.append(name)
            bypass_cap_dict[name] = port.get("bpcap")
            bw[name] = port.get("bw")
            mtu_dict[name] = port.get("mtu")
            name_list.append(name)
        for v in net_data.get("bport", {}).values():
            name_list.append(v["name"])
            bpslot_dict[v["name"]] = v.get("bpslot")
            b_pid_dict[v["name"]] = v.get("bpid")
            bypass_cap_dict[v["name"]] = v.get("bpcap")
            bw[v["name"]] = v.get("bw")
            mtu_dict[v["name"]] = v.get("mtu")
            addr_dict[v["name"]] = v.get("addr")
    except Exception as e:
        add_log(f"hw config load err: {e}")

    @classmethod
    def get_db_data(cls):
        add_log("start get db data...")
        try:
            with DbOperator(db='ng_firewall') as jarvis:
                sql = """select `name`, `port_type`, `work_mode`, `bypass_cap` from %s;""" % cls.Table
                eths = jarvis.execute_and_fetchall(sql)
            add_log(f"db data is: {eths}")
        except Exception as e:
            eths = []
            add_log(f"can not get data from db, using yaml instead.")
        return eths

    @classmethod
    def set_it(cls):
        db_data = cls.get_db_data()
        if db_data:
            cls.issued_bypass_db()
        else:
            cls.issued_bypass_config()

    @classmethod
    def issued_bypass_db(cls):
        add_log(f"start set bypass according db")
        add_log(f"slot mapping ---------->: {cls.bpslot_dict}")
        try:
            bp_slot_pid_groups = []
            for item in cls.get_db_data():
                name = item[0]
                port_type = item[1]
                if port_type == "mport":
                    continue
                work_mode = item[2]
                bp_slot = cls.bpslot_dict[name]
                b_pid = cls.b_pid_dict[name]
                if (bp_slot, b_pid) in bp_slot_pid_groups:
                    continue
                bypass_cap = item[3]
                if bypass_cap and work_mode == 0:
                    cls.set_cy_bypass("runtime", bp_slot, b_pid, value=1)
                    bp_slot_pid_groups.append((bp_slot, b_pid))
                # if bypass_cap and work_mode != 0:
                #     cls.set_cy_bypass("runtime", bp_slot, b_pid, value=0)
                #     bp_slot_pid_groups.append((bp_slot, b_pid))
        except Exception as e:
            add_log(f"bypass下发异常: {e}")

    @classmethod
    def issued_bypass_config(cls):
        add_log(f"start set bypass according yaml")
        add_log(f"slot mapping ---------->: {cls.bpslot_dict}")
        try:
            bp_slot_pid_groups = []
            for name in cls.name_list:
                port_type = 'mport' if name in cls.mport_list else 'bport'
                if port_type == "mport":
                    continue
                bp_slot = cls.bpslot_dict[name]
                b_pid = cls.b_pid_dict[name]
                if (bp_slot, b_pid) in bp_slot_pid_groups:
                    continue
                if cls.bypass_cap_dict.get(name, 1):
                    cls.set_cy_bypass("runtime", bp_slot, b_pid, value=1)
                    bp_slot_pid_groups.append((bp_slot, b_pid))
        except Exception as e:
            add_log(f"bypass setting error:{e}")

    @classmethod
    def set_cy_bypass(cls, mode, slot, b_pid, value=0):
        cmd = f"cy_bypass {mode} {slot} {b_pid} {value}"
        add_log(f"dong ------------->cmd:{cmd}")
        execute_cmd(cmd)
        time.sleep(0.1)


def make_alarm(process_name, email_data = ''):
    if process_name not in ['sv_ngifw', 'sv_mw', 'sv_logd', 'sv_usbupgrade']:
        return
    if process_name == "sv_ngifw":
        process_name = "chorplat"
    try:
        if os.path.exists(SYSLOG_ALARM):
            sysconfig_log.info(f"{process_name}进程异常", "CRIT")
            sysconfig_log.info(f"{process_name}进程恢复正常", "WARNING")
        if os.path.exists(EMAIL_ALARM):
            subject = f"「{process_name}」故障重启，请定位问题~"
            if not email_data:
                email_data = '请结合日志进行问题排查。'
            sendmail(msg=email_data, subject=subject)
    except Exception as e:
        add_log(f"make_alarm exception: {e}")


def main():
    while 1:
        # transition from ACKNOWLEDGED to READY
        add_log('*********restarting********')
        write_stdout('READY\n')
        add_log('*********im ready********')
        # read header line and print it to stderr
        line = sys.stdin.readline()
        add_log('*********im read line********')
        add_log('header:' + line)

        # read event payload and print it to stderr
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len']))
        payload = dict([x.split(':') for x in data.split()])
        add_log('payload:' + str(payload))
        # if os.path.exists("/data/flags/pm-notice-flag") and \

        if headers['eventname'] == 'PROCESS_STATE_EXITED':
            email_data = ''
            if payload['processname'] == SV_NGIFW:
                try:
                    email_data = error_detail(payload['pid'])
                    add_log(f'log_{payload["pid"]}_detail: ----{data}-----')
                except Exception as e:
                    add_log('----get  error detail failed-----')
                    add_log(str(traceback.format_exc()))
                    email_data = 'unknown error'
            make_alarm(process_name=payload['processname'], email_data=email_data)

        # set bypass when chorplat is down.
        if headers['eventname'] == 'PROCESS_STATE_EXITED' or \
                        headers['eventname'] == 'PROCESS_STATE_STOPPED':
            if payload['processname'] == SV_NGIFW:
                execute_cmd('touch /data/flags/sys-mon-fwd-err')
                try:
                    NetWorkManagerBase.set_it()
                except Exception as e:
                    add_log(f"bypass exception: {e}")

        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')

if __name__ == '__main__':
    main()
