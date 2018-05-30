# -*- coding: utf-8 -*-
import scrapy
import os
from xinlannews.items import XinlannewsItem

class NewspiderSpider(scrapy.Spider):
    name = "newspider"
    # allowed_domains = [""]
    start_urls = (
        'http://news.sina.com.cn/guide/',
    )

    def parse(self, response):
        bodys = response.xpath('//div[@id="tab01"]/div')
        items = []
        for each_parent in bodys:
            item = XinlannewsItem()
            #获取父级的url和title
            parent_url = each_parent.xpath('./h3/a/@href').extract()
            parent_title = each_parent.xpath('./h3/a/text() | ./h3/span/text()').extract()
            item['parentUrl'] = parent_url
            item['parentTitle'] = parent_title
            #获取子级的url和title
            sub_url = each_parent.xpath('./ul/li/a/@href').extract()
            sub_title = each_parent.xpath('./ul/li/a/text()').extract()


            parent_path='./data/'+parent_title[0]

            # if not os.path.exists(parent_path):
            #     os.makedirs(parent_path)
            for i in range(0, len(sub_url)):
                if sub_url[i] == 'http://roll.news.sina.com.cn/chart/index.shtml':
                    pass
                else:
                    sub_path = parent_path+'/'+sub_title[i]
                    if not os.path.exists(sub_path):
                        os.makedirs(sub_path)    #os.makedirs可以根据路径创建前面缺少的文件夹
                    # print sub_path
                    item['subUrl'] = sub_url[i]
                    item['subTitle'] = sub_title[i]
                    item['subFilename'] = sub_path

                    # items.append(item)

                    yield scrapy.Request(url=sub_url[i], meta=item, callback=self.second_parse)
                #获取子级的url和title

    def second_parse(self,respond):
        titleurl=respond.xpath('//a/@href').extract()
        item = respond.meta
        for each_article in titleurl:
            if each_article.startswith('http://news.sina.com.cn') & each_article.endswith('.shtml'):
              yield scrapy.Request(url=each_article,meta=item,callback=self.end_parse)


    def end_parse(self,respond):
        print respond.meta
        Url=respond.url
        # title = respond.xpath('/html/body/div[6]/h1/text()').extract
        print Url
        item = XinlannewsItem()
        item['parentTitle'] = respond.meta['parentTitle']
        item['parentUrl'] = respond.meta['parentUrl']
        item['subTitle'] = respond.meta['subTitle']

        item['subUrl'] = respond.meta['subUrl']
        item['article'] = Url
        title = respond.xpath('//h1/text()').extract()[0]
        content = respond.xpath('//div[@class="article"]')
        contenta = content.xpath('string(.)').extract()[0]

        item['subFilename'] = respond.meta['subFilename']+'/'+title
        item['article'] = title
        item['content'] = contenta
        print title,contenta
        yield item
        pass
