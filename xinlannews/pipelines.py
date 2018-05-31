# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import codecs

class XinlannewsPipeline(object):
    def __init__(self):
        print '@'*50
        pass

    def process_item(self, item, spider):
        self.filename = codecs.open(item['subFilename'] + '.txt', 'w', encoding='utf-8')
        self.filename.write(item['content'])
        self.filename.close()
        print '#$'*50
        return item
    def close_spider(self,spider):

        print '已写好'