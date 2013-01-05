# coding: utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from apkSpider.items import ApkItem

class CoolApkSpider(BaseSpider):
    name="coolapk"
    allowed_domains=["coolapk.com"]
    start_urls=["http://www.coolapk.com/game/5511/"]

    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        values=hxs.select('//div[@id="apkMetaInfo"]/ul')
        item=ApkItem()
        item['name']=values.select('li[1]/em/text()').extract()
        item['packageName']=values.select('li[2]/em/text()').extract()
        item['version']=values.select('li[3]/em/text()').extract()
        item['category']=values.select('li[4]/em/text()').extract()
        item['size']=values.select('li[5]/em/text()').extract()
        item['lastUpdated']=values.select('li[6]/em/text()').extract()
        item['tags']=values.select('li[6]/em/text()').extract()
        return item
