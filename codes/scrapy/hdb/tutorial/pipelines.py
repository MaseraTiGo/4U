# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from random import randint
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class TutorialPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # return 'fuck/%s.jpg' % randint(0, 100)
        sub_dir, pic_name = request.url.split('/')[-2:]
        return sub_dir + '/' + pic_name

    # def get_media_requests(self, item, info):
    #     return [Request(x) for x in item.get(self.images_urls_field, [])]
    # def process_item(self, item, spider):
    #     return item
