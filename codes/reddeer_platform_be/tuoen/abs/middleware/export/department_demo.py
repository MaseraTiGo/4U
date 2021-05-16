# coding=UTF-8

from tuoen.sys.utils.common.single import Single
from tuoen.abs.middleware.export.base import ExportDateBase


class DepartmentExport(ExportDateBase):

    def get_exec_desc(self):
        return "部门列表导出"

    def get_export_line(self):
        return ['部门id', '部门名称']

    def get_page_size(self):
        return 1000

    def get_type(self):
        return "department"

    def get_type_name(self):
        return "部门"

    def get_export_file_name(self):
        return "export_department"

    def handle_data(self, department_qs):
        result_list = [[1, "公司"]]
        '''
        current_page = 1
        department_qs = department_qs.order_by("create_time")
        while True:
            export_data = list(
                department_qs[(current_page - 1) * self.get_page_size():current_page * self.get_page_size()])
            if len(export_data) == 0:
                break
            for department in export_data:
                item = [department.id,
                        department.name,
                        department.parent_id]
                result_list.append(item)
            current_page += 1
        '''
        return result_list


department_export_middleware = DepartmentExport()
