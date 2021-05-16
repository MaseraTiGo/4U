# coding=UTF-8

import sys


class Config(object):
    classify = None

    @classmethod
    def platform_classify(cls):
        raise NotImplemented("you must implement ->[platform_label]<- in your own config")

    @property
    def use_templates(self):
        raise NotImplemented('you must implement ->[use_templates]<- in your own config')

    @classmethod
    def config_details_mapping(cls):
        raise NotImplemented("you must implement ->[config_details_mapping]<- in your own config")
