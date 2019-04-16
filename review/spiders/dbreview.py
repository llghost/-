# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.response.html import HtmlResponse
from ..items import ReviewItem
from scrapy_redis.spiders import RedisCrawlSpider

class DbreviewSpider(RedisCrawlSpider):
    name = 'dbreview'
    allowed_domains = ['douban.com']
    #start_urls = ['http://douban.com/']
    #start_urls = ['https://movie.douban.com/subject/26636712/comments?start=0&limit=20']
    redis_key = 'dbreview:start_urls'
    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_item', follow=False),
    )#爬取回来的页面中 包含url 是 start=开头后面接数字的 就加入到待爬取队列中

    def parse_item(self, response:HtmlResponse):
        #item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        print('-' * 30)
        comment = '//div[@class="comment-item"]//span[@class="short"]/text()'
        reviews=response.xpath(comment).extract()
        for review in  reviews:
            print(review)
            item=ReviewItem()
            item["review"]=review.strip()
            yield item
        #return item
