# coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from apkSpider.items import ApkItem
from scrapy.http import Request

class ApkDownloadsSpider(CrawlSpider):
    name="apkdownloads"
    allowed_domains=["apkdownloads.com|play.google.com"]
    start_urls=["http://www.apkdownloads.com"]
    #rules=[Rule(SgmlLinkExtractor(allow=[r'/2013_\d{2}_\d{2}_archive.html']),follow=True),Rule(SgmlLinkExtractor(allow=[r'/2013/\d{2}/.+?\.html']),callback='parse_game')]
    rules=[Rule(SgmlLinkExtractor(allow=[r'/2013_01_11_archive.html']),follow=True),Rule(SgmlLinkExtractor(allow=[r'/2013/\d{2}/.+?\.html']),callback='parse_game')]

    def parse_game(self,response):
        hxs=HtmlXPathSelector(response)
        values=hxs.select('//div[@class="post hentry"]/div[2]/div[1]/a/@href').extract()
        googleUrl=values[0]
        downloadUrl=values[1]
        yield Request(url=googleUrl,callback=self.parse_google)

    def parse_google(self,response):
        hxs=HtmlXPathSelector(response)
        item=ApkItem()
        #html_title
        html_title=hxs.select('//div[@class="doc-banner-container"]')
        item['name']=html_title.select('.//h1[@class="doc-banner-title"]/text()').extract()
        item['company']=html_title.select('.//a[@class="doc-header-link"]/text()').extract()
        item['apkicon']=html_title.select('//div[@class="doc-banner-icon"]/img/@src').extract()
        #html_rate
        html_rate=hxs.select('//div[@class="user-ratings"]')[0]
        item['rate']=html_rate.select('.//div[@class="average-rating-value"]/text()').extract()
        item['votes']=html_rate.select('.//div[@class="votes"]/text()').extract()
        #about the app
        html_about=hxs.select('//dl[@class="doc-metadata-list"]')
        item['datePublished']=html_about.select('.//time[@itemprop="datePublished"]/text()').extract()
        item['currentVersion']=html_about.select('.//dd[@itemprop="softwareVersion"]/text()').extract()
        item['os']=html_about.select('.//dd[4]/text()').extract()
        item['category']=html_about.select('.//dd[5]/a/text()').extract()
        item['numDownloads']=html_about.select('.//dd[6]/text()').extract()
        item['fileSize']=html_about.select('.//dd[7]/text()').extract()
        item['price']=html_about.select('.//dd[8]/text()').extract()
        #image
        item['bannerimage']=hxs.select('//div[@class="doc-banner-image-container"]/img/@src').extract()
        item['screenshot']=hxs.select('//img[@class="doc-screenshot-img"]/@src').extract()
        #video
        item['video']=hxs.select('//div[@class="doc-video-section"]/object/embed/@src').extract()
        #description
        item['description']=hxs.select('//div[@id="doc-original-text"]').extract()
        #whatsnew
        item['whatsnew']=hxs.select('//div[@class="doc-whatsnew-container"]').extract()
        print item
        return item
