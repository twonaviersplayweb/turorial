# -*- coding: utf-8 -*-

__author__ = 'yooner'


from scrapy.spider import Spider
from scrapy.selector import Selector
from turorial.items import DmozItem



class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["book.douban.com"]
    start_urls = [
        'https://book.douban.com/tag/%E7%BC%96%E7%A8%8B'
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath("//li[@class='subject-item']")
        items = []
        for site in sites:
            item = DmozItem()
            title = strip_list(site.xpath('div[2]/h2/a/text()').extract())[0]
            subtitle = strip_list(site.xpath('div[2]/h2/a/span/text()').extract())
            item['name'] = title + subtitle[0] if subtitle else title
            item['pub'] = strip_list(site.xpath('div[2]/div[1]/text()').extract())[0]
            item['description'] = strip_list(site.xpath('div[2]/p/text()').extract())[0].replace('\n', '')
            item['img_url'] = site.xpath('div[1]/a/@href').extract()[0]
            print(item)
            items.append(item)
        return items


def strip_list(list):
    return [ i.strip() for i in list if len(i) > 4]