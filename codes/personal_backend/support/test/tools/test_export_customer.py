# coding=UTF-8

import unittest
import json
import xlwt

from model.store.model_role import Organization, Operator


class TestCrawlerServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ywg_crawler(self):
        """ export customer """
        attr_list = ['来源', '店铺名称', '类目', '行业', '经营者', '网站', '城市', '地点', '联系人', '固定电话',
                     '手机', '微信', '备注']
        result_list = [attr_list]
        for operator in Operator.query():
            if operator and operator.organization:
                info = []
                info.append(operator.organization.get_source_display())
                info.append(operator.organization.name)
                info.append(operator.organization.category)
                info.append(operator.organization.industry)
                info.append(operator.organization.relative)
                info.append(operator.organization.site)
                info.append(operator.organization.city)
                info.append(operator.organization.address)
                info.append(operator.name)
                info.append(operator.tel)
                info.append(operator.phone)
                info.append(operator.wx)
                remark = ""
                if operator.organization.remark:
                    remark_dict = json.loads(operator.organization.remark)
                    remark = '\n'.join(':'.join(map(str, [key,value])) for key, value in remark_dict.items())
                info.append(remark)
                result_list.append(info)

        import math
        size = 2000
        cycle = int(math.ceil(len(result_list) / size))

        for index in range(cycle):
            temp_result_list = result_list[index * size: (index + 1) * size]
            wb = xlwt.Workbook()
            sheet = wb.add_sheet("义乌购客户信息")
            for _row, infos in enumerate(temp_result_list):
                for _col, field in enumerate(infos):
                    sheet.write(_row, _col, field)
            wb.save('ywg-{}.xls'.format(index))








