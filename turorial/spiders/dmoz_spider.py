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
        sites = sel.xpath('//ul[@class="subject-list"]/li[@class="subject-item"]/div[@class="info"]')
        items = []
        print('111111#######################')
        print(sites)
        
        with open('result', 'wb') as f:
            f.write(response.body)

        for site in sites:
            item = DmozItem()
            item['name'] = site.xpath('h2/a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            print(item)
            items.append(item)
        return items
