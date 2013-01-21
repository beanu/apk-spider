# coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from apkSpider.items import ApkItem
from scrapy.http import Request
from play import parse_google

class CoolApkSpider(CrawlSpider):
    name="coolapk"
    allowed_domains=["coolapk.com"]
    start_urls=["http://www.coolapk.com/game"]
    rules=[Rule(SgmlLinkExtractor(allow=[r'game/\?p=\d+']),follow=True),Rule(SgmlLinkExtractor(allow=[r'game/\d{4}']),callback='parse_game')]

    def parse_game(self,response):
        hxs=HtmlXPathSelector(response)
        googleUrl=hxs.select('//span[@class="caption"]/a/@href').extract()
        downloadUrl=hxs.select('//a[@class="pDown"]/@href').extract()
        downloadUrl[0]="www.coolapk.com"+downloadUrl[0]
        yield Request(url=googleUrl,meta={'downloadUrl': downloadUrl,'comefrom':'coolapk'},callback=parse_google)