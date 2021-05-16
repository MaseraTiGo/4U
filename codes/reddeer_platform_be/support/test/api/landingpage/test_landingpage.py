# -*- coding: UTF-8 -*-
# Author: Dongjd
# FileName: test_landingpage
# DateTime: 2020/12/14 16:31
# Project: operate_backend_be
# Do Not Touch Me!

import json
import hashlib

from support.common.testcase.api_test_case import APITestCase


class TestLandingPage(APITestCase):

    # def test_landing_page_list(self):
    #     api = 'landingpage/list'
    #     current_page = 1
    #     result = self.access_api(api=api, current_page=current_page)
    #     print('\n', result)

    # def test_landing_page_copy(self):
    #     api = 'landingpage/copy'
    #     landing_page_id = 2
    #     copy_name = 'heislulj'
    #     result = self.access_api(api=api, landing_page_id=landing_page_id, copy_name=copy_name)
    #     print('\n', result)

    # def test_landing_page_rename(self):
    #     api = 'landingpage/rename'
    #     landing_page_id = 1
    #     new_name = 'bastard'
    #     result = self.access_api(api=api, landing_page_id=landing_page_id, new_name=new_name)
    #     print('\n', result)

    # def test_landing_page_status_change(self):
    #     api = 'landingpage/statuschange'
    #     landing_page_id = 1
    #     status = 3
    #     result = self.access_api(api=api, landing_page_id=landing_page_id, status=status)
    #     print('\n', result)

    def test_landing_page_create(self):
        api = 'landingpage/create'

        create_info = json.loads("""{
    "name": "新的投放页测试表单1",
    "components": [
        {
            "c_type": 0,
            "index": 0,
            "attrs": {
                "rightArr": [
                    {
                        "imgurl": "http://reddeer.oss-cn-beijing.aliyuncs.com/source%2Fdefault%2F4786_1610356237.png",
                        "imgchecked": false,
                        "imgselect": "1",
                        "imginput": "",
                        "channelvalue": "1",
                        "channelurl": ""
                    }
                ]
            }
        },
        {
            "c_type": 2,
            "index": 1,
            "attrs": {
                "rightArr": [
                    {
                        "imgurl": "提交",
                        "imgchecked": false,
                        "imgselect": "1",
                        "imginput": "",
                        "channelvalue": "1",
                        "channelurl": ""
                    }
                ],
                "isFixed": true
            }
        },
        {
            "c_type": 3,
            "index": 2,
            "attrs": {
                "rightArr": {
                    "name": "新的表单",
                    "is_limited": false,
                    "is_title_hide": false,
                    "components": [
                        {
                            "name": "姓名",
                            "describe": "",
                            "index": 0,
                            "is_needed": true,
                            "tag": 0,
                            "c_type": 1,
                            "attrs": {
                                "value": "",
                                "checklist": [],
                                "list": []
                            }
                        },
                        {
                            "name": "手机",
                            "describe": "",
                            "index": 1,
                            "is_needed": true,
                            "tag": 1,
                            "c_type": 1,
                            "attrs": {
                                "value": "",
                                "checklist": [],
                                "list": []
                            }
                        }
                    ]
                }
            }
        }
    ]
}""")
        result = self.access_api(api=api, create_info=create_info)
        print('\n', result)

    # def test_landing_page_get(self):
    #     api = 'landingpage/get'
    #     landing_page_id = 63
    #     result = self.access_api(api=api, landing_page_id=landing_page_id)
    #     print('\n', result)

#     def test_landing_page_edit(self):
#         api = 'landingpage/edit'
#         landing_page_id = 22
#         edit_info = json.loads(
#             """{
#     "name": "fxkingshit22",
#     "components": [
#         {
#             "c_type": 3,
#             "index": 0,
#             "attrs": {
#                 "rightArr": {
#                     "name": "新的表单DD",
#                     "is_limited": false,
#                     "is_title_hide": false,
#                     "components": [
#                         {
#                             "name": "手机001",
#                             "describe": "",
#                             "index": 0,
#                             "is_needed": true,
#                             "tag": 1,
#                             "c_type": 1,
#                             "attrs": {
#                                 "value": "",
#                                 "checklist": [],
#                                 "list": []
#                             },
#                             "id": 461
#                         },
#                         {
#                             "name": "年龄",
#                             "describe": "",
#                             "index": 1,
#                             "is_needed": true,
#                             "tag": 2,
#                             "c_type": 1,
#                             "attrs": {
#                                 "value": "",
#                                 "checklist": [],
#                                 "list": []
#                             },
#                             "id": 462
#                         },
#                         {
#                             "name": "姓名",
#                             "describe": "",
#                             "index": 2,
#                             "is_needed": true,
#                             "tag": 0,
#                             "c_type": 1,
#                             "attrs": {
#                                 "value": "",
#                                 "checklist": [],
#                                 "list": []
#                             },
#                             "id": 463
#                         },
#                         {
#                             "name": "性别",
#                             "describe": "",
#                             "index": 3,
#                             "is_needed": true,
#                             "tag": 3,
#                             "c_type": 2,
#                             "attrs": {
#                                 "value": "1",
#                                 "checklist": [],
#                                 "list": [
#                                     {
#                                         "name": "男",
#                                         "label": "1",
#                                         "isCheck": false,
#                                         "isclose": false
#                                     },
#                                     {
#                                         "name": "女",
#                                         "label": "2",
#                                         "isCheck": false,
#                                         "isclose": false
#                                     },
#                                     {
#                                         "name": "（保密）",
#                                         "label": "3",
#                                         "isCheck": false,
#                                         "isclose": false
#                                     }
#                                 ]
#                             },
#                             "id": 464
#                         }
#                     ],
#                     "id": 133
#                 }
#             }
#         }
#     ]
# }"""
#         )
#         result = self.access_api(api=api, landing_page_id=landing_page_id, edit_info=edit_info)
#         print('\n', result)

    # def test_landing_page_copy(self):
    #     api = 'landingpage/publish'
    #     landing_page_id = 79
    #     result = self.access_api(api=api, landing_page_id=landing_page_id)
    #     print('\n', result)

    ...
