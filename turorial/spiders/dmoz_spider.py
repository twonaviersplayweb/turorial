# -*- coding: utf-8 -*-

__author__ = 'yooner'

import re
from scrapy.selector import Selector
from turorial.items import DmozItem
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from urllib.parse import unquote

class DmozSpider(CrawlSpider):
    name = "dmoz"
    allowed_domains = ["book.douban.com"]
    start_urls = [
        'https://book.douban.com/tag/%E7%BC%96%E7%A8%8B',
        'https://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91',
        'https://book.douban.com/tag/%E6%97%85%E8%A1%8C'
    ]

    rules = (
        #Rule(LinkExtractor(allow=(''))),
        Rule(LinkExtractor(allow=('/tag/\w+\?start=\d0?\d')), callback="parse_item"),

    )

    def parse_item(self, response):
        sel = Selector(response)
        sites = sel.xpath("//li[@class='subject-item']")
        url_prefix = 'https://book.douban.com'
        items = []
        item = {}
        tag_unquote = unquote(response.url.split('/')[-1])
        tag = re.search('(\w+)?', tag_unquote).group(0)

        for site in sites:
            item = DmozItem()
            title = strip_list(site.xpath('div[2]/h2/a/text()').extract())[0]
            subtitle = strip_list(site.xpath('div[2]/h2/a/span/text()').extract())
            item['name'] = title + subtitle[0] if subtitle[0] != 'none' else title
            item['pub'] = strip_list(site.xpath('div[2]/div[1]/text()').extract())[0]
            item['description'] = strip_list(site.xpath('div[2]/p/text()').extract())[0].replace('\n', '')
            item['img_url'] = site.xpath('div[1]/a/@href').extract()[0]
            item['tag'] = tag
            items.append(item)
            yield item

        '''
        next_url = sel.xpath('//*[@id="subject_list"]/div[2]/span[4]/a/@href').extract()[0]
        print(next_url)
        if next_url and int(re.search('\d+', next_url).group(0)) < 120:
            url = url_prefix + next_url
            yield Request(url, callback=self.parse)
        '''
def check_list(arg_type):
    def make_wrapper(func):
        def wrapper(*args, **kwarg):
            if len(args[0]) > 0:
                return func(*args, **kwarg)
            else:
                new_args = tuple(['None'])
                return func(*new_args, **kwarg)
        return wrapper
    return make_wrapper

@check_list(list)
def strip_list(list1):
    test_list = [ i.strip() for i in list1 if len(i) > 4] if list1 else ['none']
    if test_list:
        return test_list
    return ['none']
