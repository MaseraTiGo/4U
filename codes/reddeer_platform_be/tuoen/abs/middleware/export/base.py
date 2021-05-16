# coding=UTF-8

import csv
import datetime
import threading
import random
from urllib import parse

import pandas as pd

from tuoen.abs.middleware.export.loader import ExportHelper
from tuoen.abs.middleware.extend.oss import OSSAPI
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.cache.redis import redis


class ExportDateBase(object):

    @staticmethod
    def check_redis_name(redis_name):
        # redis.delete(redis_name)
        try:
            result_redis = redis.get(redis_name)
            if result_redis is not None:
                return True
        except Exception as e:
            print(e)
            return False
        return False

    def get_type(self):
        raise NotImplementedError('Please export_element this interface in subclass')

    def get_type_name(self):
        raise NotImplementedError('Please export_element this interface in subclass')

    def get_export_file_name(self):
        raise NotImplementedError('Please export_element this interface in subclass')

    def get_redis_name(self):
        redis_name = "export_{type}".format(type=self.get_type())
        return redis_name

    def get_csv_name(self):
        csv_name = "%s%s.xlsx" % (self.get_type_name(), datetime.datetime.now().strftime('%Y%m%d%H%M'))
        return csv_name

    # def get_csv_path(self, name):
    #     cur_path = os.path.dirname(os.path.abspath(__file__))
    #     file_path = r"%s\%s" % (cur_path, self.get_export_file_name())
    #     if not os.path.exists(file_path):
    #         os.mkdir(file_path)
    #     csv_name = r"%s\%s.csv" % (file_path, name)
    #
    #     return csv_name

    def get_csv_path(self, name):

        import os
        from django.conf import settings
        return os.path.join(settings.STATIC_FILES_ROOT, 'awesome_dong', name)

    def run(self, object_qs):
        redis_name = self.get_redis_name()
        if self.check_redis_name(redis_name):
            raise BusinessError("请不要重复导出")
        redis.set(redis_name, 1)
        self.csv_name = self.get_csv_name()
        test_thread = threading.Thread(target=self.export, args=(redis_name, self.csv_name, object_qs))
        test_thread.start()

    def export_old(self, redis_name, csv_name, object_qs):
        try:
            export_type = self.get_type()
            # csv_name = self.get_csv_name()
            csv_path = self.get_csv_path(csv_name)
            csv_file3 = open(csv_path, 'w', newline='', encoding='utf-8')
            writer2 = csv.writer(csv_file3)
            writer2.writerow(self.get_export_line())
            data_list = self.handle_data(object_qs)
            for data in data_list:
                writer2.writerow(data)
            csv_file3.close()
            redis.delete(redis_name)
            # url = csv_path
            '''上传OSS
            url = self.push_oss(csv_path, csv_name, export_type)
            url = parse.unquote_plus(url)
            '''
            # ExportHelper.create(**{"name": "{name}.csv".format(name=csv_name),
            #                        "type": export_type, "url": url})
        except Exception as e:
            print("---------->>>导出异常", e)
        redis.delete(redis_name)

    def process_data_list(self, data_list):
        for data in data_list:
            detail_info = data[-1]
            info = ''
            for k, v in detail_info.items():
                info += '{}: {}'.format(k, v)
                info += '   \n'
            data[-1] = info

    def export(self, redis_name, csv_name, object_qs):
        try:
            export_type = self.get_type()
            csv_path = self.get_csv_path(csv_name)
            data_list = self.handle_data(object_qs)
            data_list.insert(0, self.get_export_line())
            data_df = pd.DataFrame(data_list)
            writer = pd.ExcelWriter(csv_path, engine='xlsxwriter')
            data_df.to_excel(writer, header=None, index=False)
            worksheet = writer.sheets['Sheet1']
            worksheet.set_column("A:F", 33)
            writer.save()
            redis.delete(redis_name)
            self.push_oss(csv_path, csv_name, export_type)
        except Exception as e:
            print("---------->>>导出异常", e)
        redis.delete(redis_name)

    def handle_data(self, object_qs):
        raise NotImplementedError('Please implement this interface in subclass')

    def push_oss(self, csv_path, csv_name, export_type):
        url = ""
        oss_file_path = "export/{type}/{csv_name}".format(type=export_type, csv_name=csv_name)
        with open(csv_path, 'rb') as f:
            url = OSSAPI().put_object(oss_file_path, f, "reddeer")
            url = parse.unquote_plus(url)
        self.url = url

    def get_new_download(self):
        search_info = {"type": self.get_type()}
        export = ExportHelper.get_new(**search_info)
        return export
