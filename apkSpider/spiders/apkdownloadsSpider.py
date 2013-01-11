# coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from apkSpider.items import ApkItem

class ApkDownloadsSpider(CrawlSpider):
    name="apkdownloads"
    allowed_domains=["apkdownloads.com"]
    start_urls=["http://www.apkdownloads.com"]
    #rules=[Rule(SgmlLinkExtractor(allow=[r'/2013_\d{2}_\d{2}_archive.html']),follow=True),Rule(SgmlLinkExtractor(allow=[r'/2013/\d{2}/.+?\.html']),callback='parse_game')]
    rules=[Rule(SgmlLinkExtractor(allow=[r'/2013_01_10_archive.html']),follow=True),Rule(SgmlLinkExtractor(allow=[r'/2013/\d{2}/.+?\.html']),callback='parse_game')]

    def parse_game(self,response):
        hxs=HtmlXPathSelector(response)
        values=hxs.select('//div[@class="post hentry"]/div[2]/div[1]/a/@href').extract()
        googleUrl=values[0]
        downloadUrl=values[1]
        yield Request(url=googleUrl,callback=self.parse_google)

    def parse_google(self,response):
        hxs=HtmlXPathSelector(response)
        #title
        div_title=hxs.select('//div[@class="doc-banner-container"]')
        apkname=div_title.select('h1[@class="doc-banner-title"]/text()').extract()
        company=div_title.select('a[@class="doc-header-link"]/text()').extract()
        apkicon=div_title.select('div[@class="doc-banner-icon"]/img/@src').extract()
        price=div_title.select('span[@class="buy-button-price"]/text()').extract()

