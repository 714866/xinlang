# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XinlannewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #父级内容
    parentTitle = scrapy.Field()
    parentUrl = scrapy.Field()

    #子级内容
    subTitle = scrapy.Field()
    subUrl = scrapy.Field()
    subFilename = scrapy.Field()
    #文章内容
    articleUrl = scrapy.Field()
    article = scrapy.Field()
    content = scrapy.Field()
    pass
