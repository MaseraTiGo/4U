# -*- coding: utf-8 -*-
# file_name       : parse_txt.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2020/8/1 10:36

# ********************************************************
# update: add comments details --- 20200802 DS
# ********************************************************

import re
from copy import deepcopy

# third party package. using "pip install pandas" to install.
import pandas as pd


def get_request_or_response_details(cur_i, lines):
    """
    :param cur_i: current index of lines.
    :param lines: txt lines(not null).
    :return: the details of request or response.
    """
    detail = ""
    for line in lines[cur_i:]:
        if re.search("^}.*", line):
            detail += line
            break
        else:
            detail += line
    return detail


def parse_txt_2_2_dimensional_list(file_path: str):
    """
    :param file_path: the src file of txt.
    :return: two dimensional list include pre-processing data.
    """
    rows = []
    with open(file_path, encoding="utf-8") as f:
        lines = [line for line in f.readlines() if len(line.strip('\r\n').strip('\n').strip())]

    # save single row info, include operate type, request info and response info.
    cur_row = []

    # when processing response detail info. this flag will be used as the end of current row info.
    end_row_flag = False

    # when the value of this flag is true that's saying the next several lines are the details of request or response.
    detail_flag = False

    # entering loop.
    for index, line in enumerate(lines):
        if detail_flag:
            detail = get_request_or_response_details(index, lines)
            cur_row.append(detail)
            detail_flag = False
            if end_row_flag:
                rows.append(deepcopy(cur_row))
                cur_row = []
                end_row_flag = False
        # if the current line and next line are starts with alphabets or Chinese character, then the current line will
        # be the operate-type.
        if pattern.search(line) and pattern.search(lines[index + 1]):
            cur_row.append(line)
            continue
        if "request" in line.lower() or "response" in line.lower():
            detail_flag = True
        if "response" in line.lower():
            end_row_flag = True
    return rows


def write_2_excel(data_s, path=r'.\output.xlsx'):
    """
    :param data_s: data that be processed by the func of parse_txt_2_excel.
    :param path: output excel path.
    :return: nothing.
    """
    # insert the title of the sheet.
    data_s.insert(0, title)
    writer = pd.ExcelWriter(path)
    data_frame = pd.DataFrame(data_s)
    data_frame.to_excel(writer, header=None, index=False)
    writer.save()


if __name__ == "__main__":
    # src txt file
    src_file = r'E:\Temp\mqtt.txt'

    # output excel path
    output_excel = r'E:\Temp\mqtt.xlsx'

    # excel sheet header
    title = ['operate', 'request', 'response']

    pattern = re.compile("^[a-z|A-Z|\u4e00-\u9fa5]+")

    ds = parse_txt_2_2_dimensional_list(src_file)
    write_2_excel(ds, output_excel)
