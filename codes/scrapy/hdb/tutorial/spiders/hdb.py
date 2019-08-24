# -*- coding: utf-8 -*-
# file_name       : hdb.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/8/22 8:58
import scrapy

from ..items import HDBItem

flag = 0


def add_or_not(fn):
    def wrapper_add_or_not(*args, **kwargs):
        res = fn(*args, **kwargs)
        global flag
        if flag == 1:
            flag -= 1
        else:
            flag += 1
            res = str(int(res) - 1)
        return res

    return wrapper_add_or_not


@add_or_not
def add_one(x):
    return str(int(x.group()) + 1)


class HDBSpider(scrapy.Spider):
    name = 'hdb'
    # main_url = 'http://www.hdbss.com'
    # start_urls = ['http://www.hdbss.com/article-list-id-%d.html' % i for i in range(6, 12)]
    origin_url = 'http://www.hdbss.com/article-list-id-%s.html'
    allowed_domains = ['hdbss.com']

    def start_requests(self):
        # for url in self.start_urls:
        #     yield scrapy.Request(url, dont_filter=True)
        cs = CustomService()
        cs.run()
        pages = cs.pages
        kinds = cs.kinds
        self.start_urls = [self.origin_url % i for i in kinds]
        extend_urls = []
        if int(pages) > 1:
            for url in self.start_urls:
                for i in range(2, int(pages) + 1):
                    extend_urls.append(url.split('.html')[0] + '-page-%s.html' % i)
        self.start_urls.extend(extend_urls)
        # ==================================================================================
        # for i in self.start_urls:
        #     print('url----------------->', i, '\n')
        # a = input('*' * 88)
        # if a == 'q':
        #     import sys
        #     sys.exit()
        # ==================================================================================
        while self.start_urls:
            url = self.start_urls.pop(0)
            yield scrapy.Request(url, dont_filter=True)
            # new_url = ''
            # while 1:
            #     print('new_url is ----------------->', new_url, '\n')
            #     if '-page-' in new_url:
            #         new_url = re.sub('(?P<num>\d+)', add_one, url)
            #     else:
            #         new_url = url.split('.html')[0] + '-page-2.html'
            #     try:
            #         requests.get(new_url)
            #     except Exception as _:
            #         pass
            #     else:
            #         if '-page-%s' % pages in new_url:
            #             break
            #         self.start_urls.append(new_url)

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        result = self.single_web_page_url(response)
        for i in result:
            category, url = i
            url = self.main_url + url
            yield scrapy.Request(url=url, callback=self.img_parse, cb_kwargs={'category': category})

    def img_parse(self, response, **kwargs) -> dict:
        img_urls = response.xpath("//img[contains(@src, 'http://i.imagseur.com/uploads')]")
        for i in img_urls:
            item = HDBItem()
            pics_url = i.re(".+src=\"(.+jpg).+")
            item['pics'] = pics_url
            item['category'] = kwargs.get('category', '.')
            yield item

    def single_web_page_url(self, response) -> tuple:
        origin_list = response.xpath("//a[contains(@href, '/article-show')]")
        for single_url in origin_list:
            yield single_url.xpath('.//text()').extract()[-1], single_url.re(".+href=\"(.+html).+target.+")[0]


class CustomService(object):
    _color_table = {
        'white': 0,
        'red': 1,
        'green': 2,
        'yellow': 3,
        'blue': 4,
        'purple': 5,
        'cyan': 6,
        'prey': 7,
    }

    kinds = []
    pages = 3

    def pprint(self, string, color='white'):
        i = self._color_table.get(color, 0)
        print("\033[0;3%dm%s\033[0m" % (i, string))
        print('\n')

    def run(self):
        print('=' * 88)
        category = ''''
                    little wolf, you are here again.
            6 --->自拍偷拍   7 --->亚洲色图   8 --->欧美色图
            9 --->美腿丝袜   10--->清纯优美   11--->淑女乱伦
            and, what's more? here is Million Zhao's favorite!
                           13--->变态另类
            you can choose like this:
            eg:
            6 7 10 11
            remember separator should be space!
        '''
        print(category)
        print('=' * 88)
        kinds = input('now , make your fucking choice!\n')
        pages = input('one more thing, how many pages you wanna download default is 3 pages\n')
        self.kinds = kinds.split()
        self.pages = pages if pages else self.pages
        print("----------------------now , wait, it will be soon---------------------------")

    def kind(self):
        pass

    def pages(self):
        pass

    def tbd(self):
        pass
