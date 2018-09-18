# -*- coding: utf-8 -*-

# file   name: 4 zy
# file   func: auto calculate time
# file author: ds
# file   date: 2018-09-18

import time
import datetime
import re
import os
from selenium import webdriver

'''this py file just for calculating work time'''


class WorkTimeCal(object):
    """all start here"""
    _user = '51282'
    _password = '6-yNtsi7'
    _url = r'http://ics.chinasoftosg.com/SignOnServlet'
    _current_month = 0
    _user_work_days = 0
    _need_seconds = 0

    def __init__(self):
        pass

    @classmethod
    def open_chrome(cls):
        """open chrome for login in"""
        driver = webdriver.Chrome()
        driver.get(cls._url)
        driver.maximize_window()
        cls.login(driver)

    @classmethod
    def login(cls, driver):
        """logging---"""
        time.sleep(1)
        driver.find_element_by_xpath("//input[@name='userName']").clear()
        driver.find_element_by_xpath("//input[@name='userName']").send_keys(cls._user)
        driver.find_element_by_xpath("//input[@id='password']").clear()
        driver.find_element_by_xpath("//input[@id='password']").send_keys(cls._password)
        driver.find_element_by_xpath("//input[@type='button']").click()
        cls.jump_to_time_page(driver)

    @classmethod
    def jump_to_time_page(cls, driver):
        """jump to the work order page"""
        driver.find_element_by_xpath(
            "//a[@href='http://oa.chinasoftosg.com:8888/sso.route?target=c3lzdGVtL2ZyYW1lLzQvaW5kZXguanNw']").click()
        driver.switch_to_window(driver.window_handles[-1])
        # here can replace with auto wait
        time.sleep(3)
        driver.find_element_by_xpath("//a[@menuname='考勤']").click()
        time.sleep(3)
        # driver.refresh()
        driver.find_element_by_xpath("//a[contains(@href, '个人打卡')]").click()
        time.sleep(3)
        data_src_list = driver.find_elements_by_xpath("//tr[contains(@id, 'maingrid')]/td[contains(@id, 'c')]")
        print('stop here=============>')
        # cls.parse_html_data(data_src_list)

    @classmethod
    def parse_html_data(cls, data):
        pass

    @classmethod
    def get_file(cls):
        """get the src data from txt file"""
        file_list = []
        for _, _, files in os.walk('.'):
            file_list = [file for file in files if file.endswith('txt')]
        if file_list.__len__() != 1:
            print('may there has no txt file or not only one , check it!')
            import sys
            sys.exit()
        file_name = file_list[0]
        with open(file_name, 'r') as f:
            cls.process_data(f)

    @classmethod
    def process_data(cls, f):
        """process the source data"""
        lines = f.readlines()
        new_data_list = [lines[i: i + 7] for i in range(0, len(lines), 7)]
        cls._user_work_days = len(new_data_list)
        cls._need_seconds = cls._user_work_days * 8 * 60 * 60
        total_seconds = 0
        for per_data in new_data_list:
            per_data = list(map(lambda x: x.strip('\r').strip('\r\n'), per_data))
            this_month = per_data[4] + ' '
            s_time = per_data[5]
            e_time = per_data[6]
            start_time = s_time if s_time else '08:30'
            t_start_time = this_month + start_time
            end_time = e_time if e_time else '18:00'
            t_end_time = this_month + end_time
            total_seconds += cls.get_seconds(t_start_time, t_end_time)
            print(this_month, 'work time: %.2f' % ((cls.get_seconds(t_start_time, t_end_time) / 3600) - 1.5))
        total_seconds = total_seconds - cls._user_work_days * 1.5 * 3600
        cls.print_result(total_seconds)

    @classmethod
    def get_seconds(cls, s, e):
        """format datetime and get the seconds"""
        s_second = time.mktime(time.strptime(s, '%Y-%m-%d %H:%M'))
        e_second = time.mktime(time.strptime(e, '%Y-%m-%d %H:%M'))
        return e_second - s_second

    @classmethod
    def print_result(cls, seconds):
        """nothing but print the result out"""
        print('当前计算工作天数', cls._user_work_days)
        print('当前工时超出：%.2fh' % ((seconds - cls._need_seconds) / 3600))


if __name__ == '__main__':
    wtc = WorkTimeCal()
    wtc.get_file()
    # wtc.open_chrome()
