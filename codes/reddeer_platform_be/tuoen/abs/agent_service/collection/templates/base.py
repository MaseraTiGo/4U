# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: base
# DateTime: 1/28/2021 5:09 PM
# Project: awesome_dong
# Do Not Touch Me!

import abc
import datetime
import os
import pathlib
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib import parse
from zipfile import ZipFile
import time

import pandas as pd
import requests
from django.conf import settings

from tuoen.abs.agent_service.collection import AttachmentExportType
from tuoen.abs.middleware.extend.oss import OSSAPI
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.cache.redis import redis


class BaseExport(abc.ABC):
    EXPORT_DIR = 'awesome_dong'
    MID = '反馈信息收集表'

    def __init__(self, name, company, classify, num, data, push=True):
        self.url = None
        self._name = name
        self._data = data
        self._num = num
        self._company = company
        self._classify = classify
        self._push = push
        self._mid = ''
        self.temp_path = os.path.join(settings.STATIC_FILES_ROOT, self.EXPORT_DIR,
                                      self.export_name_stem + str(time.time_ns()))

    @property
    @abc.abstractmethod
    def export_file_type(self):
        """"""

    @abc.abstractmethod
    def run(self, *args):
        """must implement your codes here"""

    @staticmethod
    def is_exporting(export_name):
        try:
            result_redis = redis.get(export_name)
            if result_redis is not None:
                return True
        except Exception as e:
            print(e)
            return False
        return False

    @property
    def export_name_in_redis(self):
        redis_name = "export_{type}".format(type=self.export_name)
        return redis_name

    @property
    def export_name(self):
        sections = {
            'prefix': self._name,
            'mid': self.MID if not self._mid else self._mid,
            'suffix': datetime.datetime.now().strftime('%Y%m%d'),
            'type_': self.export_file_type
        }
        return '{prefix}_{mid}_{suffix}.{type_}'.format(**sections)

    @property
    def export_name_stem(self):
        return pathlib.Path(self.export_name).stem

    @property
    def local_path(self):
        # return os.path.join(settings.STATIC_FILES_ROOT, self.EXPORT_DIR, self.export_name_stem)
        return self.temp_path

    @classmethod
    def is_existed_or_create(cls, path):
        p = pathlib.Path(path)
        if not p.exists():
            p.mkdir(parents=True)

    @property
    def oss_path(self):
        """oss path"""
        return "{0}/collection/{1}/{2}".format(self._company, self._classify, self._num)

    def push_oss(self, local_path, oss_path, export_name):
        if not self._push:
            return
        oss_file_path = "export/{oss_path}/{export_name}".format(oss_path=oss_path, export_name=export_name)
        with open(local_path, 'rb') as f:
            url = OSSAPI().put_object(oss_file_path, f, "reddeer")
            url = parse.unquote_plus(url)
        self.url = url

    def clear_up(self):
        redis.delete(self.export_name_in_redis)
        import shutil
        try:
            os.remove(self.local_path + f'.{self.export_file_type}')
        except:
            ...
        shutil.rmtree(self.local_path, ignore_errors=True)

    def fuck_it(self, *args):
        if not self._data:
            raise BusinessError('当前查询无记录可供导出！')
        if self.is_exporting(self.export_name_in_redis):
            raise BusinessError("请不要重复导出")
        redis.set(self.export_name_in_redis, 1)
        test_thread = threading.Thread(target=self.run, args=args)
        test_thread.start()


class BaseExcelTemplate(BaseExport):
    NAME = 'base_excel_template'
    UNIQUE_NUM = 100

    DEFAULT_HEADERS = ['序号', '提交时间']

    def __init__(self, name, company, classify, num, data, headers, push=True, mid=None):
        super().__init__(name, company, classify, num, data, push=push)
        self.url = None
        self._headers = headers
        self._push = push
        self._mid = mid
        self._workbook = None
        self._worksheet = None

    @property
    def export_file_type(self):
        return 'xlsx'

    @property
    def headers(self):
        """the header of current template"""
        return self.DEFAULT_HEADERS + list(self._headers)

    @property
    def header_format(self):
        return self._workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#AABBCC',
            'border': 1})

    def format_excel(self):
        self._worksheet.set_column(0, 15)
        self._worksheet.set_column("B:Z", 30)
        self._worksheet.set_default_row(20)
        self._worksheet.set_row(0, 30)

    def process(self):
        """pre process of the data"""
        all_data = []

        for index, customer in enumerate(self._data, 1):
            item = [
                       index,
                       customer.create_time,
                   ] + [customer.detail_data.get(attr, '-') for attr in self._headers]
            all_data.append(item)
        self._data = all_data

    def run(self):
        try:
            self.process()
            self._data.insert(0, self.headers)
            data_df = pd.DataFrame(self._data)
            self.is_existed_or_create(self.local_path)
            file_path = os.path.join(self.local_path, self.export_name)
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
            data_df.to_excel(writer, header=None, index=False, startrow=0)
            self._workbook = writer.book
            self._worksheet = writer.sheets['Sheet1']
            self.format_excel()
            redis.delete(self.export_name_in_redis)
            writer.save()
            writer.close()
            self.push_oss(file_path, self.oss_path, self.export_name)
        except Exception as e:
            print(f'dong --------------->export error:\n{e}')
        finally:
            if self._push:
                self.clear_up()


class BaseZipTemplate(BaseExport):

    def __init__(self, name, company, classify, num, data, push=True, base_path=None):
        super(BaseZipTemplate, self).__init__(name, company, classify, num, data, push=push)
        self._push = push
        if base_path:
            self.temp_path = base_path

    @property
    def export_file_type(self):
        return 'zip'

    def dir_2_fucking_zip(self, path):
        p = pathlib.Path(path)
        fuckers = p.glob(os.sep.join(['**', '*.*']))
        with ZipFile(f'{path}.{self.export_file_type}', 'w') as mother_fucker:
            for fucker in fuckers:
                zip_fucker = fucker.relative_to(self.local_path)
                mother_fucker.write(fucker, zip_fucker)

    def request_4_fucking_pic_2_local(self, shit_info, retry=3):
        url = shit_info.get('url')
        if not url:
            return
        shit_name = shit_info.get('name')
        sub_dir_name = shit_info.get('dir_name')

        res = None
        for _ in range(retry):
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    break
            except Exception as e:
                print('establish connection failed! reason --->: ', e)
        if not res:
            raise BusinessError('get pic failed!')
        if res.status_code != 200:
            raise BusinessError('get pic failed!')
        path = os.sep.join([self.local_path, sub_dir_name])
        try:
            self.is_existed_or_create(path)
        except Exception as _:
            raise BusinessError(f'create current dir: {path} failed!')
        shit_path = os.sep.join([path, shit_name])
        with open(shit_path, 'wb') as fuck:
            fuck.write(res.content)

    def generate_by_sub_export_type(self, sub_export_type):
        valid_data = []
        id_ = 1
        for customer in self._data:
            for key, value in customer.detail_data.items():
                if not isinstance(value, dict) or value.get('type') not in ['pic', 'attach']:
                    continue
                if sub_export_type == AttachmentExportType.BY_CUSTOMER:
                    value['dir_name'] = str(id_)
                else:
                    value['dir_name'] = key
                name = value['imgName'].split('.') if 'imgName' in value else value['fileName'].split('.')
                value['name'] = f'{".".join(name[0: -1])}_{id_}.{name[-1]}' \
                    if sub_export_type == AttachmentExportType.BY_QUESTION else f"{'.'.join(name)}"
                valid_data.append(value)
            id_ += 1
        self._data = valid_data
        with ThreadPoolExecutor() as shit:
            shit.map(self.request_4_fucking_pic_2_local, self._data)

    def run(self, sub_export_type):
        try:
            self.generate_by_sub_export_type(sub_export_type)
            redis.delete(self.export_name_in_redis)
            self.dir_2_fucking_zip(self.local_path)
            self.push_oss(self.local_path + '.' + self.export_file_type, self.oss_path,
                          self.export_name)
        except Exception as e:
            print(f'dong --------------->export zip error:\n{e}')
        finally:
            self.clear_up()
