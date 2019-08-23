# -*- coding: utf-8 -*-
# file_name       : hdb.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/8/22 8:58
import scrapy

from ..items import HDBItem


class HDBSpider(scrapy.Spider):
    name = 'hdb'
    main_url = 'http://www.hdbss.com'
    start_urls = ['http://www.hdbss.com/article-list-id-%d.html' % i for i in range(6, 12)]
    # start_urls = ['http://www.hdbss.com/article-list-id-8.html']
    allowed_domains = ['hdbss.com']

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        page_urls = [self.main_url + i for i in self.single_web_page_url(response)]
        for url in page_urls:
            yield scrapy.Request(url=url, callback=self.img_parse)

    def img_parse(self, response):
        img_urls = response.xpath("//img[contains(@src, 'http://i.imagseur.com/uploads')]")
        item = HDBItem()
        for i in img_urls:
            pics_url = i.re(".+src=\"(.+jpg).+")
            item['pics'] = pics_url
            yield item

    def single_web_page_url(self, response) -> list:
        origin_list = response.xpath("//a[contains(@href, '/article-show')]")
        urls = []
        for item in origin_list:
            urls.extend(item.re(".+href=\"(.+html).+target.+"))
        return urls
