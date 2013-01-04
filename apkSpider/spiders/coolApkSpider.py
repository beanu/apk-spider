# coding: utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
class CoolApkSpider(BaseSpider):
    name="coolapk"
    allowed_domains=["coolapk.com"]
    start_urls=["http://www.coolapk.com/game/5511/"]
    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        values=hxs.select('//div[@id="apkMetaInfo"]/ul/li')
        for value in values:
            print value.select('em/text()').extract()
