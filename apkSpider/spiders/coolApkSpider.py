# coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from apkSpider.items import ApkItem

class CoolApkSpider(CrawlSpider):
    name="coolapk"
    allowed_domains=["coolapk.com"]
    start_urls=["http://www.coolapk.com/game"]
    rules=[Rule(SgmlLinkExtractor(allow=[r'game/\?p=\d+']),follow=True),Rule(SgmlLinkExtractor(allow=[r'game/\d{4}']),callback='parse_game')]

    def parse_game(self,response):
        hxs=HtmlXPathSelector(response)
        values=hxs.select('//div[@id="apkMetaInfo"]/ul')
        item=ApkItem()
        item['name']=values.select('li[1]/em/text()').extract()
        item['packageName']=values.select('li[2]/em/text()').extract()
        item['version']=values.select('li[3]/em/text()').extract()
        item['category']=values.select('li[5]/em/text()').extract()
        item['size']=values.select('li[7]/em/text()').extract()
        item['lastUpdated']=values.select('li[8]/em/text()').extract()
        item['tags']=values.select('li[9]/em/a/text()').extract()
        return item
