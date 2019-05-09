# -*- coding: utf-8 -*-
# file_func  : split big files for my YBEr
# file_author: 'Johnathan.Wick'
# file_date  : '5/7/2019 5:38 PM'

"""
if u don't know how to use, contact me or search 'parser_parser' in this file , you will get enough info for help.
good luck
"""

# modify_history: 5/8/2019 9:04 AM last modify

import argparse
import os
import time
from math import ceil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def get_big_file(threshold, f_type, f_path):
    pre_files = []
    targets = [f_path] if len(f_path) == 1 else f_path.split(';')
    for target in targets:
        if os.path.isfile(target):
            pre_files.append(target)
            continue
        pre_files.extend(
            [str(f) for f in Path(target).glob('**\\*%s' % f_type) if os.path.getsize(str(f)) >= threshold])
    return pre_files


def split_files(fucking_big_file):
    file_name = fucking_big_file.split(os.sep)[-1].split('.')
    with open(fucking_big_file, 'rb') as fucking_damn_work:
        write_to_fucking_little(fucking_damn_work, *file_name)


def write_to_fucking_little(big_obj, name, kind):
    lines = big_obj.readlines()
    nums = int(ceil(len(lines) / single_size))
    for i in range(nums):
        new_file_name = os.sep.join([output, name + '_%d.%s' % (i, kind)])
        with open(new_file_name, 'wb') as f:
            f.writelines(lines[single_size * i:single_size * (i + 1)])


def parser_parser():
    parser = argparse.ArgumentParser(description='some useless info')
    parser.add_argument('--threshold', '-t', type=int, default=50,
                        help='File size over threshold will be split, based on Mb')
    parser.add_argument('--suffix', '-s', type=str, default='txt',
                        help='File\'s suffix name, in other words, that\'s file type')
    parser.add_argument('--limit', '-l', type=int, default=10_000,
                        help='how many lines you wanna set in a single new file')
    parser.add_argument('--path', '-p', type=str, default='.', help='use ";" to split them')
    parser.add_argument('--output', '-o', type=str, default=os.sep.join(['.', 'output']),
                        help='path that you wanna new file be')
    args = parser.parse_args()
    return args.threshold, args.suffix, args.limit, args.path, args.output


if __name__ == '__main__':
    s = time.time()
    split_threshold, file_type, single_size, path_file, output = parser_parser()
    if not os.path.exists(output):
        os.makedirs(output)
    file_list = get_big_file(split_threshold * 1024 * 1024, file_type, path_file)
    print(file_list)
    with ThreadPoolExecutor() as pool:
        pool.map(split_files, file_list)
    print('total cost %s' % (time.time() - s,))
