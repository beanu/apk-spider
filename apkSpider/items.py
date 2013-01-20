# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ApkItem(Item):
    # define the fields for your item here like:
    name = Field()
    packageName = Field()
    company = Field()
    #rate
    rate = Field()
    votes = Field()
    #about
    datePublished = Field()
    currentVersion = Field()
    os = Field()
    category = Field()
    numDownloads = Field()
    fileSize = Field()
    price = Field()
    #image
    apkicon = Field()
    bannerimage = Field()
    screenshot = Field()
    #video
    video = Field()
    #description
    description = Field()
    #whatsnew
    whatsnew = Field()
    #other
    tags = Field()
    downloadUrl = Field()
    comefrom = Field()
