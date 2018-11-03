# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class novelItem(scrapy.Item):
    #每本书的名字
    book_name= scrapy.Field()
    #每一章节的路径
    link_url = scrapy.Field()
    # 每一章的章节名
    dir_name = scrapy.Field()
    # 每一章的内容
    dir_content = scrapy.Field()
    pass
