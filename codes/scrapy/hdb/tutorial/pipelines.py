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
        pic_name = request.url.split('/')[-1]
        return request.item_path + '/' + pic_name

    def get_media_requests(self, item, info):
        for x in item.get(self.images_urls_field, []):
            request = Request(x)
            request.item_path = item.get('category', '.')
            yield request

    # def process_item(self, item, spider):
    #     self._path = item['category']
    #     return item
