# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: test_collection
# DateTime: 2020/12/15 16:17
# Project: awesome_dong
# Do Not Touch Me!

import json
from support.common.testcase.api_test_case import APITestCase


class TestCollection(APITestCase):

    def test_collection_list(self):
        api = 'collection/list'
        current_page = 1
        query_info = json.dumps({
            'landing_page_id': 45,
        })
        result = self.access_api(api=api, current_page=current_page, query_info=query_info)
        print('\n', result)

    def test_collection_export(self):
        api = 'collection/export'
        query_info = json.dumps({
            'landing_page_id': 45,
            # 'start_time': '2020-01-01 00:00:00',
            # 'end_time': '2021-01-01 00:00:00'
        }
        )
        result = self.access_api(api=api, query_info=query_info)
        print('\n', result)

    def test_collection_collection(self):
        api = 'collection/collectinfo'
        collect_info = {
            "landing_page_id": 45,
            "detail_data": {
                "form_data": [{
                    "id": 111,
                    "name": "表单001",
                    "collections": [{
                        "name": "姓名",
                        "value": "Aston",
                        "tag": 0,
                        "type": 1,
                        "checklist": [],
                        "list": []
                    },
                        {
                            "name": "性别",
                            "value": "0",
                            "tag": 3,
                            "type": 2,
                            "checklist": [],
                            "list": [{
                                "label": "男"
                            }]
                        },
                        {
                            "name": "地址",
                            "value": "湖北省武汉市江夏区关顾软件园",
                            "tag": 6,
                            "type": 3,
                            "checklist": [],
                            "list": []
                        },
                        {
                            "name": "年龄",
                            "value": 133,
                            "tag": 4,
                            "type": 1,
                            "checklist": [],
                            "list": []
                        },
                        {
                            "name": "找培训班你最关注什么？",
                            "value": "",
                            "checklist": ["0", "1", "2"],
                            "tag": 7,
                            "type": 4,
                            "list": [{
                                "label": "别的家长对班主任的评价",
                            },
                                {
                                    "label": "上课体验",
                                },
                                {
                                    "label": "售后服务"
                                }
                            ]
                        }
                    ]
                }]
            },
        }

        result = self.access_api(api=api, is_auth=False, collect_info=collect_info)
        print('\n', result)

    def test_collection_template_list(self):
        api = 'collection/templatelist'
        result = self.access_api(api=api)
        print('\n', result)
