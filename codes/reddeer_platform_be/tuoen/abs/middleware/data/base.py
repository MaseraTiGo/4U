# coding=UTF-8

import math
import time
import datetime
import xlrd
from xlrd import xldate_as_tuple
import threading

from tuoen.sys.utils.cache.redis import redis

from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField
from tuoen.sys.utils.common.split_page import Splitor
from model.store.model_import import ImportStatus


class ExcelDateTimeField(BaseField):

    def exec_excel(self, value):
        if not value:
            value = Null
        else:
            date = xldate_as_tuple(value, 0)
            value = datetime.datetime(*date)
        return value

    def exec_string(self, value, fmt):
        return datetime.datetime.strptime(value, fmt)

    def exec_successive(self, value):
        return self.exec_string(value, '%Y%m%d%H%M%S')

    def exec_standards(self, value):
        return self.exec_string(value, '%Y-%m-%d %H:%M:%S')

    def exec_standards_half(self, value):
        return self.exec_string(value, '%Y-%m-%d')

    def exec_half(self, value):
        return self.exec_string(value, '%Y%m%d')

    def exec_slash(self, value):
        return self.exec_string(value, '%Y/%m/%d %H:%M')

    def exec_slash_half(self, value):
        return self.exec_string(value, '%Y/%m/%d')

    def exec_point_half(self, value):
        return self.exec_string(value, '%Y.%m.%d')

    def parsing(self, value):
        result = None

        for helper in (self.exec_excel, self.exec_standards, self.exec_standards_half, self.exec_successive, \
                       self.exec_half, self.exec_slash, self.exec_slash_half, self.exec_point_half):
            try:
                result = helper(value)
                break
            except Exception as e:
                pass
        '''
        if result is None:
            raise Exception("excel datatime format error")
        '''
        return result

    def formatting(self, value):
        if not isinstance(value, datetime.datetime):
            raise debugerror()
        return value.strftime("%y-%m-%d %h:%m:%s")


class ExcelDeletePointField(BaseField):

    def parsing(self, value):
        if not value:
            return ""
        return str(value).split('.')[0]

    def formatting(self, value):
        return str(value)


class ExcelMoneyField(BaseField):

    def parsing(self, value):
        if not value:
            return 0
        return int(float(value) * 100)

    def formatting(self, value):
        return str(round(value / 100, 2))


class BaseImport(object):

    def get_object_byid(self, id):
        object = self.get_exec_cls().get_byid(id)
        if object is None:
            raise BusinessError("该信息不存在")
        return object

    def update_object(self, object, **attr):
        object.update(**attr)
        return True

    def get_exec_cls(self):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def get_fields(self):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def read(self, f):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def search_qs(self, **search_info):
        search_qs = self.get_exec_cls().query(**search_info)
        if "create_time_start" in search_info:
            search_qs = search_qs.filter(create_time__gte=search_info["create_time_start"])
        if "create_time_end" in search_info:
            search_qs = search_qs.filter(create_time__lt=search_info["create_time_end"])
        search_qs = search_qs.order_by("-id")
        return search_qs

    def search(self, current_page, **search_info):
        search_qs = self.search_qs(**search_info)
        page = Splitor(current_page, search_qs)

        page.is_converting = self.check_redis()
        return page

    def check_redis(self):
        is_converting = False
        redis_name = self.get_redis_name()
        try:
            redis.get(redis_name)
            is_converting = True
        except Exception as e:
            pass
        return is_converting

    def get_convert_list(self, **search_info):
        search_info.update({"status": "init"})

        search_qs = self.search_qs(**search_info)
        return search_qs

    def exec_convet(self):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def check(self, row_list):
        fields = self.get_fields()
        row_infos = DictWrapper({})
        error_infos = {}
        for index, field in enumerate(fields):
            cell = row_list[index]
            if isinstance(cell, str):
                cell = cell.strip()
            key, helper = fields[index]
            try:
                row_infos.update({key: helper.parse(cell)})
            except Exception as e:

                error_infos.update({key: [helper, index]})

        error_msg = ""
        if error_infos:
            error_info_list = [helper.get_desc() \
                               for helper, _ in error_infos.values()]
            error_msg = ', '.join(error_info_list)
        return row_infos, error_msg

    def store(self, data_infos):
        obj = self.get_exec_cls()()
        for key, value in data_infos.items():
            setattr(obj, key, value)
        return obj
        # return self.get_exec_cls().create(**data_infos)

    def get_queue(self, queue_len, size=100):
        cycle = int(math.ceil(queue_len / size))
        for index in range(cycle):
            yield index * size, (index + 1) * size

    def run(self, f):
        import_list, error_list = self.read(f)
        if error_list:
            # print('check error ', error_list)
            return [], error_list

        obj_list = []
        queue_len = len(import_list)
        for start, end in self.get_queue(queue_len):
            store_list = []
            for import_data in import_list[start:end]:
                store = self.store(import_data)
                store_list.append(store)
            cur_obj_list = self.get_exec_cls() \
                .objects.bulk_create(store_list)
            obj_list.extend(cur_obj_list)

        return obj_list, error_list

    def convert_prepare(self, convert_list):
        return convert_list, []

    def convert(self, **search_info):
        t = time.time()

        redis_name = self.get_redis_name()
        is_redis_exist = False
        try:
            redis.get(redis_name)
            is_redis_exist = True
            # redis.delete(redis_name)
        except Exception as e:
            redis.set(redis_name, 1)
            test_thread = threading.Thread(target=self.convert_in, args=(redis_name,), kwargs=search_info)
            test_thread.start()

        if is_redis_exist:
            raise BusinessError("该任务已存在请不要重复转化")
        print(time.time() - t)
        print("----------------------------->baseconvert done")

        return [], []

    def convert_after(self, success_list, failed_list):
        return success_list, failed_list

    def convert_in(self, redis_name, **search_info):
        convert_list = self.get_convert_list(**search_info)
        if len(convert_list) == 0:
            redis.delete(redis_name)
            return [], []

        exec_list, fail_list = self.convert_prepare(convert_list)
        success_list, failed_list = [], fail_list

        over_time = 60 * 60 * 6
        first_time = time.time()

        for index, convert_obj in enumerate(exec_list):
            now_time = time.time()
            if now_time - first_time > over_time:
                break
            convert_obj.update(status=ImportStatus.EXCUTTING)
            try:
                is_success, error_text = self.exec_convet(convert_obj)
            except Exception as e:
                print("--------------------------->exception", e)
                convert_obj.update(status=ImportStatus.FAILED, error_text="系统异常，请联系管理员")
                failed_list.append(convert_obj)
                redis.delete(redis_name)
            else:
                if is_success:
                    convert_obj.update(status=ImportStatus.FINISH)
                    success_list.append(convert_obj)
                else:
                    convert_obj.update(status=ImportStatus.FAILED, error_text=error_text)
                    failed_list.append(convert_obj)
            print("convert items ---> ", index + 1)

        redis.delete(redis_name)


class ExcelImport(BaseImport):

    def read(self, f):
        if type(f) == str:
            workbook = xlrd.open_workbook(f)
        else:
            workbook = xlrd.open_workbook(file_contents=f)

        sheet_names = workbook.sheet_names()
        fields = self.get_fields()
        data_list, error_list = [], []
        for sheet_name in sheet_names:
            sheet = workbook.sheet_by_name(sheet_name)
            print("====", sheet.ncols, len(fields))
            if sheet.ncols != len(fields):
                error = '表结构错误'
                error_list.append(error)
                break

            for row_index in range(1, sheet.nrows, 1):
                row = sheet.row_values(row_index)
                row_infos, error_msg = self.check(row)
                if error_msg:
                    error = "[ {row}row ]: {error} format error" \
                        .format(row=row_index, error=error_msg)
                    error_list.append(error)
                else:
                    data_list.append(row_infos)
        return data_list, error_list
