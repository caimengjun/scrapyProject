# -*- coding: utf-8 -*-
import scrapy

from jinyong.items import novelItem


class NovelSpider(scrapy.Spider):
    name = 'novel'


    def __init__(self):
        #链接头
        self.server_link = 'http://www.jinyongwang.com'
        self.allowed_domains = ['jinyongwang.com/book/']
        self.start_urls = ['http://www.jinyongwang.com/book/']


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        book_list = response.xpath("//*[@id='main']/div[2]/ul/li")
        #找到每一本书的a标签，放到一个列表中
        for book in book_list:
            hrefs = book.xpath(".//p[1]/a/@href").extract()
            new_hrefs = self.server_link + "".join(hrefs)
            yield scrapy.Request(url=new_hrefs, callback=self.parse2,meta={"new_hrefs": new_hrefs},dont_filter=True)

    def parse2(self, response):
        new_hrefs = response.meta['new_hrefs']
        menus = response.xpath("//*[@id='pu_box']/div[3]/ul/li/a/@href").extract()
        # 把每个章节的路径放到列表中
        items = []
        for menu in menus:
            item = novelItem()
            item["book_name"] = response.xpath("//*[@id='pu_box']/div[3]/div[1]/h1/span/text()").extract_first()
            item["link_url"] = self.server_link + menu
            items.append(item)


        for item in items:
            yield scrapy.Request(url=item['link_url'], meta={"item": item}, callback=self.parse3,dont_filter=True)

    def parse3(self, response):
        item = response.meta["item"]
        item["dir_name"] = response.xpath("//*[@id='title']/text()").extract_first()
        content = response.xpath("//*[@id='vcon']/p/text()").extract()
        item["dir_content"] = " ".join(content)
        yield item





