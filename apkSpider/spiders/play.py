from scrapy.selector import HtmlXPathSelector
from apkSpider.items import ApkItem

def parse_google(response):
    downloadUrl=response.meta['downloadUrl']
    comefrom=response.meta['comefrom']
    hxs=HtmlXPathSelector(response)
    item=ApkItem()
    item['downloadUrl']=downloadUrl
    item['packageName']=response.url[response.url.find('id=')+3:response.url.find('&')]
    item['comefrom']=comefrom
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
    return item