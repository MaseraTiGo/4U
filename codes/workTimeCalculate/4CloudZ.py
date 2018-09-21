# -*- coding: utf-8 -*-

# file   name: 4 zy
# file   func: auto calculate time
# file author: ds
# file   date: 2018-09-18

import datetime
import os
import re
import requests
import time
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from seleniumrequests import Chrome

'''
    this py file just for calculating work time.
    Known bugs:
    No.1:
        After the login is successful, jump to the oa page is slow, very slow!
    No.2:
        data of  8-21 is missing, but does not affect the results.
    ......    
'''


class ZyError(Exception):
    """exception self define"""
    _msg = 'error'

    def __init__(self, msg):
        # Exception.__init__(self, msg)
        super().__init__(self)
        self._msg = msg

    def __str__(self):
        return self._msg


class WorkTimeCal(object):
    """all start here"""
    _user = '51282'
    _password = '6-yNtsi7'
    _url = r'http://ics.chinasoftosg.com/SignOnServlet'
    _url_final = "http://kq.chinasoftosg.com/workAttendance/importsExamineAction_getImportsExamine"
    _url_test = 'http://oa.chinasoftosg.com:8888/system/frame/4/index.jsp'
    _current_month = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m')
    _user_work_days = 0
    _need_seconds = 0
    _headers = {'Accept': 'application / json, text / javascript, * / *',
                'Accept - Encoding': 'gzip, deflate',
                'Accept - Language': 'en - US, en; q = 0.9',
                'Connection': 'keep - alive',
                'Content - Type': 'application / x - www - form - urlencoded',
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
                'X-Requested-With': 'XMLHttpRequest'
                }
    _simple_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
    }

    def __init__(self):
        pass

    @classmethod
    def open_chrome(cls):
        """open chrome for login in"""
        driver = Chrome()
        driver.get(cls._url)
        driver.maximize_window()
        cls.login(driver)

    @classmethod
    def login(cls, driver):
        """logging---"""
        driver.find_element_by_xpath("//input[@name='userName']").clear()
        driver.find_element_by_xpath("//input[@name='userName']").send_keys(cls._user)
        driver.find_element_by_xpath("//input[@id='password']").clear()
        driver.find_element_by_xpath("//input[@id='password']").send_keys(cls._password)
        driver.find_element_by_xpath("//input[@type='button']").click()
        cls.jump_to_time_page(driver)
        # respone = driver.request('get', cls._url_test, headers=cls._simple_headers)
        # respone = driver.request('post', cls._url_final, data=data, headers=cls._simple_headers)
        # cookies = driver.get_cookies()
        # cls.requests_cookies_get(cookies)

    @classmethod
    def requests_cookies_get(cls, cookies):
        """no use!"""
        s = requests.session()
        verify = False
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
        data = {
            'importsExamineVo.page': 1,
            'importsExamineVo.pagesize': 25
        }
        s.get(cls._url_final, verify=verify, cookies=jar, headers=cls._headers, data=data)

    @classmethod
    def jump_to_time_page(cls, driver):
        """jump to the work order page"""
        time.sleep(1)
        driver.find_element_by_xpath("//a[contains(@href, 'c3lzdGVtL2ZyYW1lLzQvaW5kZXguanNw')]").click()
        driver.switch_to_window(driver.window_handles[-1])
        # here can replace with auto wait
        time.sleep(1)
        driver.find_element_by_xpath("//a[@menuname='考勤']").click()
        time.sleep(2)
        # driver.refresh()
        frame = driver.find_elements_by_xpath("//iframe")[1]
        driver.switch_to_frame(frame)
        # WebDriverWait(driver, 10).until(driver.find_element_by_xpath("//a[contains(@href, '个人打卡')]"))
        driver.find_element_by_xpath("//a[contains(@href, '个人打卡')]").click()
        time.sleep(6)
        try:
            frame = driver.find_elements_by_xpath("//iframe")[1]
        except IndexError as _:
            raise ZyError("can get the frame, so must exit.")
        driver.switch_to_frame(frame)
        data_src_list = driver.find_elements_by_xpath("//tr[contains(@id, 'maingrid|2')]/td[contains(@id, 'c')]")
        cls.parse_html_data(data_src_list)

    @classmethod
    def parse_html_data(cls, data_list):
        """parse data return from last func"""
        data_list = [x.text for x in data_list]
        data_list_pre_process = [data_list[i: i + 7] for i in range(0, len(data_list), 7)]
        data_list_pre_process = list(filter(lambda x: cls._current_month in x[-3], data_list_pre_process))
        cls.ready_to_calculate(data_list_pre_process)

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
    def process_data_from_txt(cls, f):
        """process the source data"""
        lines = f.readlines()
        new_data_list = [lines[i: i + 7] for i in range(0, len(lines), 7)]
        cls.ready_to_calculate(new_data_list)

    @classmethod
    def ready_to_calculate(cls, new_data_list):
        """nothing but calculate"""
        cls._user_work_days = len(new_data_list)
        cls._need_seconds = cls._user_work_days * 8 * 60 * 60
        total_seconds = 0
        for per_data in new_data_list:
            per_data = list(map(lambda x: x.strip('\r').strip('\r\n'), per_data))
            this_month = per_data[4] + ' '
            s_time = per_data[5]
            e_time = per_data[6]
            start_time = s_time if s_time and s_time > '08:30' else '08:30'
            t_start_time = this_month + start_time
            end_time = e_time if e_time else '18:00'
            t_end_time = this_month + end_time
            total_seconds += cls.get_seconds(t_start_time, t_end_time)
            print(this_month, 'work time: %.2f' % (cls.get_seconds(t_start_time, t_end_time) / 3600))
        cls.print_result(total_seconds)

    @classmethod
    def get_seconds(cls, s, e):
        """format datetime and get the seconds"""
        s_second = time.mktime(time.strptime(s, '%Y-%m-%d %H:%M'))
        e_second = time.mktime(time.strptime(e, '%Y-%m-%d %H:%M'))
        r_seconds = e_second - s_second
        # the time between 6:00 pm and 6:30 pm can't be calculated
        e = e.split()[-1]
        non_mins = 90 if e >= '13:30' else 0
        if e > '18:00':
            non_mins += 30 if e >= '18:30' else int(e.split(':')[-1])
        r_seconds -= non_mins * 60
        return r_seconds

    @classmethod
    def print_result(cls, seconds):
        """nothing but print the result out"""
        print('days count in     --->:', cls._user_work_days, 'days')
        print('man-hours overflow--->：%.2fh' % ((seconds - cls._need_seconds) / 3600))


if __name__ == '__main__':
    """
    if you wanna count overwork time in , you should use get_file this func, meanwhile, don't paste those data to src txt
    """
    wtc = WorkTimeCal()
    # wtc.get_file()
    wtc.open_chrome()
