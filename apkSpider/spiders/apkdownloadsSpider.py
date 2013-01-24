# coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from apkSpider.items import ApkItem
from scrapy.http import Request
from play import parse_google

class ApkDownloadsSpider(CrawlSpider):
    name="apkdownloads"
    allowed_domains=["apkdownloads.com|play.google.com"]
    #start_urls=["http://www.apkdownloads.com"]
    start_urls=["http://www.apkdownloads.com/2013/01/race-stunt-fight-2-v111-apk.html"]
    #rules=[Rule(SgmlLinkExtractor(allow=[r'/2013_\d{2}_\d{2}_archive.html']),follow=True),Rule(SgmlLinkExtractor(allow=[r'/2013/\d{2}/.+?\.html']),callback='parse_game')]
    #rules=[Rule(SgmlLinkExtractor(allow=[r'/2013_01_11_archive.html']),follow=True),Rule(SgmlLinkExtractor(allow=[r'/2013/\d{2}/.+?\.html']),callback='parse_game')]

    def parse_game(self,response):
        hxs=HtmlXPathSelector(response)
        values=hxs.select('//div[@class="post hentry"]/div[2]/div[1]/a/@href').extract()
        googleUrl=values[0]
        downloadUrl=values[1]
        yield Request(url=googleUrl,meta={'downloadUrl': downloadUrl,'comefrom':'apkdownloads'},callback=parse_google)

    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        values=hxs.select('//div[@class="post hentry"]/div[2]/div[1]/a/@href').extract()
        googleUrl=values[0]
        downloadUrl=values[1]
        yield Request(url=googleUrl,meta={'downloadUrl': downloadUrl,'comefrom':'apkdownloads'},callback=parse_google)