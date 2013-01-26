from scrapy.spider import BaseSpider

class TopApkSpider(BaseSpider):
    name = "topapk"
    allowed_domains = ["play.google.com"]
    start_urls = [
        "https://play.google.com/store/apps/collection/topselling_free?start=%d&num=24" % x*24 for x in xrange(10)
    ]

    def parse(self, response):
    	hxs=HtmlXPathSelector(response)
        packages=hxs.select('//ul[@class="snippet-list container-snippet-list"]/li/@data-docid').extract()