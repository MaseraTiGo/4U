# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : x_web
# @Time    : 2024/9/2 14:33
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import json
import os
import re

if __name__ == '__main__':
    from django import setup

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
    setup()

    p_code = re.compile('(\d+)')

    from super_dong.models import MyShit
    shits_qs = MyShit.objects.all()
    update_obj = []
    for item in shits_qs:
        remark = item.remark
        # if "{}" not in remark and "notice" not in remark and "fcode" not in remark:
        #     print(f"dong ---------. code: {remark}")

        if "\\" in remark:
            item.remark = {}
            update_obj.append(item)
            print(f"dong ---------. code: {remark}|id: {item.id}")


        # if '{}' in remark:
        #     update_obj.append(item)
        #     item.remark = {}
        # elif "notice" in remark:
        #     update_obj.append(item)
        #     item.remark = {}
        # elif "fcode" in remark:
        #     code = p_code.findall(remark)[0]
        #     print(f"dong ---------. code: {code}")
        #     item.remark = json.dumps({"fcode": code})
        #     update_obj.append(item)
    shits_qs.bulk_update(update_obj, ('remark',))

