# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : x_web
# @Time    : 2022/12/14 13:57
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from super_dong.frame.core.data_field.data_type import RequestData, ResponseData
from super_dong.frame.core.api import AuthApi
from super_dong.frame.core.api_repo import BaseRepo


class Doc:
    pass


class ApiDocGenerator(object):
    prefix = "*"

    @classmethod
    def the_doke(cls):
        from super_dong.frame.core.protocol import initialize_api_repo_files
        initialize_api_repo_files()

        full_mapping = {}

        for service, rel_api_repo in BaseRepo.FULL_API_MAPPING.items():
            full_mapping[service] = cls.get_repo_details(rel_api_repo._INDIVIDUAL_API_MAPPING)
        return full_mapping

    @classmethod
    def get_repo_details(cls, repo):
        if not repo:
            return []
        api_info_list = []
        for name, api_cls in repo.items():
            api_info_list.append({name.replace('.', '/'): cls.gen_api_details_info(api_cls)})
        return api_info_list

    @classmethod
    def gen_api_details_info(cls, api):
        info = []
        author = f"{cls.prefix}Author"
        info.append(f"{author: <12}: {api.get_author()}")

        history = f"{cls.prefix}History"
        info.append(f"{history: <12}: {api.get_history()}")

        desc = f"{cls.prefix}Desc"
        info.append(f"{desc: <12}: {api.get_desc()}")

        api_num = f"{cls.prefix}Api_num"
        info.append(f"{api_num: <12}: {api.get_unique_num()}")

        info.append(cls._gen_request_info(api))
        info.append(cls._gen_response_info(api))
        api_info = "\n".join(info)

        return api_info

    @classmethod
    def _gen_request_info(cls, api: AuthApi):
        title = f"{cls.prefix}Request"
        ret = f"{title: <12}:\n"
        request_info = "\n".join([
            cls_.display(level=1) for cls_ in api.__dict__.values()
            if hasattr(cls_, '_superDong') and issubclass(cls_, RequestData)
        ])

        final = ret + request_info
        return final

    @classmethod
    def _gen_response_info(cls, api):
        title = f"{cls.prefix}Response"
        ret = f"{title: <12}:\n"
        request_info = "\n".join([
            cls_.display(level=1) for cls_ in api.__dict__.values()
            if hasattr(cls_, '_superDong') and issubclass(cls_, ResponseData)
        ])
        request_info = request_info if request_info else "    ..."
        final = ret + request_info
        return final
