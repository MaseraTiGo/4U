# -*- coding: utf-8 -*-
# @File    : main
# @Project : djangoProject
# @Time    : 2022/11/29 10:36
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import pathlib
import time
import zipfile

import pyzipper


def get_fucking_files(dir_='.') -> list:
    p = pathlib.Path(dir_).glob('test_codes/**/*.*')
    files = [file.__str__() for file in p]
    # print(files)
    return files


def fucking_zip_it(en=True):
    tar_path = "fucking.zip"
    password = "123456"
    dante = pyzipper.AESZipFile(tar_path, 'w', compression=pyzipper.ZIP_LZMA)
    if not en:
        dante = zipfile.ZipFile(tar_path, 'w', zipfile.ZIP_DEFLATED)

    with dante as my_zip:
        if en:
            my_zip.setpassword(password.encode())
            my_zip.setencryption(pyzipper.WZ_AES, nbits=128)
        for csv_path in get_fucking_files():
            my_zip.write(csv_path, csv_path)


def fucking_zip_it2(fuck=True):
    tar_path = "fucking.zip"
    password = "123456"
    dante = pyzipper.AESZipFile(tar_path, 'w', compression=pyzipper.ZIP_STORED)

    with dante as my_zip:
        if fuck:
            my_zip.setpassword(password.encode())
            my_zip.setencryption(pyzipper.WZ_AES, nbits=128)
        for csv_path in get_fucking_files():
            my_zip.write(csv_path, csv_path)


s = time.time()
fucking_zip_it2()
print(f"dong -------------->{time.time() - s}")
