# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProject
# @Time    : 2022/12/13 10:00
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import abc
import contextlib
import json
import mmap
import pathlib

import yaml as pyyaml
from ruamel import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

__all__ = ["JsonFileParser", "YamlFileParser"]


class BaseFileParser(abc.ABC):

    def __init__(self, file_path, mode='r'):
        if not pathlib.Path(file_path).is_file():
            raise Exception(f"no such file!: {self._file_path}")
        self._file_path = file_path

        self._mode = mode

    @property
    @abc.abstractmethod
    def data(self):
        """must be implement in your subclass"""

    @abc.abstractmethod
    def write(self, data):
        """must be implement in your subclass"""


class JsonFileParser(BaseFileParser):

    @property
    def data(self):
        with open(self._file_path, self._mode, encoding='utf8')as ironman:
            try:
                json_data = json.load(ironman)
            except Exception as e:
                print(f"open file and read failed!: {self._file_path}"
                      f"exception: {e}")
                json_data = None
            return json_data

    def write(self, data, mode='w', ensure_ascii=False):
        ans = True
        with open(self._file_path, mode, encoding='utf8')as ironman:
            try:
                json.dump(data, ironman, ensure_ascii=ensure_ascii)
            except Exception as e:
                print(f"write file failed!: {self._file_path}"
                      f"exception: {e}")
                ans = False
        return ans


class YamlFileParser(BaseFileParser):

    @property
    def data(self):
        with open(self._file_path, self._mode, encoding='utf-8') as hulk:
            try:
                yaml_data = yaml.load(hulk, Loader=yaml.RoundTripLoader)
            except Exception as e:
                print(f"open file and read failed!: {self._file_path}"
                      f"exception: {e}")
                yaml_data = None
            return yaml_data

    def write(self, data, mode='w', version=None):
        ans = True
        with open(self._file_path, mode=mode, encoding='utf-8') as hulk:
            try:
                if version:
                    yaml.dump(data, stream=hulk, Dumper=yaml.RoundTripDumper,
                              version=version)
                else:
                    yaml.dump(data, stream=hulk, Dumper=yaml.RoundTripDumper)
            except Exception as e:
                ans = False
                print(f"write file failed!: {self._file_path}"
                      f"exception: {e}")
        return ans


class PyYamlFileParser(BaseFileParser):

    @property
    def data(self):
        with open(self._file_path, self._mode, encoding='utf-8') as hulk:
            try:
                yaml_data = pyyaml.load(hulk, Loader=pyyaml.SafeLoader)
            except Exception as e:
                print(f"open file and read failed!: {self._file_path}"
                      f"exception: {e}")
                yaml_data = None
            return yaml_data

    def write(self, data, mode='w'):
        ans = True
        with open(self._file_path, "r+b") as f:  # 打开yaml_file文件
            with contextlib.closing(mmap.mmap(f.fileno(),
                                              0)) as yaml_mm:  # 创建mmap内存映射对象, 0表示映射整个文件
                yaml_mm.seek(0)  # 将yaml_mm对象对应的文件的位置移动到开始位置
                """yaml用法　https://www.cnblogs.com/klb561/p/9326677.html"""
                dict_temp = pyyaml.load(yaml_mm.read(
                    yaml_mm.size()))  # 读取yaml_mm对象映射的文件的所有内容，并且转换成类似（字典）json的格式
                try:
                    new_yaml = pyyaml.safe_dump(dict_temp,
                                                default_flow_style=False,
                                                encoding='utf-8',
                                                allow_unicode=True)
                except Exception as e:
                    ans = False
                    print(f"write file failed!: {self._file_path}"
                          f"exception: {e}")
                yaml_mm.resize(len(new_yaml))
                yaml_mm.seek(0)
                yaml_mm.write(new_yaml)
                yaml_mm.flush()
        return ans


yy = YamlFileParser('hw.yaml')
print(yy.data['affinity']['/dante/aston'])