# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProject
# @Time    : 2022/12/10 9:43
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import hashlib
from typing import List


def gen_unique_id_by_str(src: str) -> int:
    # Convert the string to bytes
    src_bytes = src.encode('utf-8')

    # Generate the hash value using SHA256 algorithm
    hash_value = hashlib.sha256(src_bytes).hexdigest()

    # Take the first 10 characters of the hash value
    hash_value_short = hash_value[:8]

    # Convert the hash value to an integer
    unique_id = int(hash_value_short, 16)

    # Return the unique ID
    return unique_id


def gen_input_box_by_attrs(attrs: List[str], b_type=None, ex_args_str=""):
    if b_type is None:
        raise ValueError(f'b_type can not be None')
    info = {}
    attr: str
    for attr in attrs:
        exec_str = f"{attr} = st.{b_type}_input('{attr.capitalize()}')"
        if ex_args_str:
            exec_str = f"{attr} = st.{b_type}_input('{attr.capitalize()}', {ex_args_str})"
        exec(f"{exec_str}", {"st": st}, info)
    return info


def gen_text_input_box_by_attrs(attrs: List[str], b_type='text'):
    return gen_input_box_by_attrs(attrs, b_type=b_type)


def gen_num_input_box_by_attrs(
        attrs: List[str],
        b_type='number', value=1, min_value=1, **extra_info
):
    extra_info.update(
        {
            "value": value,
            "min_value": min_value
        }
    )
    ex = []
    for key, val in extra_info.items():
        ex.append(f"{key}={val}")
    ex_str = ', '.join(ex)
    return gen_input_box_by_attrs(attrs, st, b_type=b_type, ex_args_str=ex_str)


class PageInfo:
    def __init__(self, page_num: int, page_size: int = 10):
        self.page_num = page_num
        self.page_size = page_size


def gen_page_input_box():
    page_number = st.number_input("Page Num", value=1, min_value=1)
    page_size = st.number_input("Page Size", value=10, min_value=1)
    return PageInfo(page_number, page_size)
