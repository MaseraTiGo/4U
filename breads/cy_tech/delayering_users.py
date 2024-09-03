# -*- coding: utf-8 -*-
# @File    : delayering_users
# @Project : 4U
# @Time    : 2024/8/23 17:28
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from copy import deepcopy
from pprint import pprint


class Fuck:

    @classmethod
    def delayer_user_and_grp(cls, datas):
        def dfs(node):
            path.append(node['name'])
            if not node['children']:
                node['belong'] = deepcopy(path)
                ret.append(node)
                yield

            if node['children']:
                for child in node['children']:
                    yield from dfs(child)
            path.pop()

        ret = []
        for data in datas:  # type: dict
            path = []
            list(dfs(data))
        return ret


if __name__ == '__main__':
    datax = [
        {
            "id": 3,
            "unique_id": 101,
            "name": "Volkswagen Group",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [],
            "children": [
                {
                    "id": 5,
                    "unique_id": 102,
                    "name": "Porsche",
                    "desc": "this is an User Grp",
                    "parent": 3,
                    "attr_parents": [],
                    "children": [
                        {
                            "id": 75,
                            "unique_id": 137,
                            "name": "ProjectX",
                            "desc": "this is an User Grp",
                            "parent": 5,
                            "attr_parents": [],
                            "children": [],
                            "category": 2,
                            "verification_method": 1,
                            "verification_detail": {
                                "password": "5201314"
                            },
                            "status": 1,
                            "ex_info": {},
                            "create_time": "2024-08-22 17:23:35"
                        },
                        {
                            "id": 76,
                            "unique_id": 138,
                            "name": "ProjectY",
                            "desc": "this is an User Grp",
                            "parent": 5,
                            "attr_parents": [],
                            "children": [],
                            "category": 2,
                            "verification_method": 1,
                            "verification_detail": {
                                "password": "5201314"
                            },
                            "status": 1,
                            "ex_info": {},
                            "create_time": "2024-08-22 17:23:35"
                        },
                        {
                            "id": 77,
                            "unique_id": 139,
                            "name": "ProjectZ",
                            "desc": "this is an User Grp",
                            "parent": 5,
                            "attr_parents": [],
                            "children": [],
                            "category": 2,
                            "verification_method": 1,
                            "verification_detail": {
                                "password": "5201314"
                            },
                            "status": 1,
                            "ex_info": {},
                            "create_time": "2024-08-22 17:23:35"
                        }
                    ],
                    "category": 2,
                    "verification_method": 1,
                    "verification_detail": {
                        "password": "5201314"
                    },
                    "status": 1,
                    "ex_info": {},
                    "create_time": "2024-08-22 15:47:25"
                },
                {
                    "id": 6,
                    "unique_id": 103,
                    "name": "Audi",
                    "desc": "this is an User Grp",
                    "parent": 3,
                    "attr_parents": [],
                    "children": [],
                    "category": 2,
                    "verification_method": 1,
                    "verification_detail": {
                        "password": "5201314"
                    },
                    "status": 1,
                    "ex_info": {},
                    "create_time": "2024-08-22 15:51:21"
                }
            ],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 15:40:38"
        },
        {
            "id": 49,
            "unique_id": 111,
            "name": "PSA Group",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:12:52"
        },
        {
            "id": 50,
            "unique_id": 112,
            "name": "Hyundai KIA",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:12:52"
        },
        {
            "id": 51,
            "unique_id": 113,
            "name": "Toyota",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:12:52"
        },
        {
            "id": 52,
            "unique_id": 114,
            "name": "General Motors",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:12:52"
        },
        {
            "id": 53,
            "unique_id": 115,
            "name": "Nissan",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:12:52"
        },
        {
            "id": 54,
            "unique_id": 116,
            "name": "Stellantis",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:12:52"
        },
        {
            "id": 55,
            "unique_id": 117,
            "name": "Renault S.A",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:12:52"
        },
        {
            "id": 56,
            "unique_id": 118,
            "name": "Fiat",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:12:52"
        },
        {
            "id": 72,
            "unique_id": 134,
            "name": "BYD",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [
                57
            ],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:25:47"
        },
        {
            "id": 73,
            "unique_id": 135,
            "name": "XiaoMi",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [
                57
            ],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:25:47"
        },
        {
            "id": 74,
            "unique_id": 136,
            "name": "GreatWall",
            "desc": "this is an User Grp",
            "parent": 1,
            "attr_parents": [
                57
            ],
            "children": [],
            "category": 2,
            "verification_method": 1,
            "verification_detail": {
                "password": "5201314"
            },
            "status": 1,
            "ex_info": {},
            "create_time": "2024-08-22 16:25:47"
        }
    ]
    pprint((Fuck.delayer_user_and_grp(datax)))
