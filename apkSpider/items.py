# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ApkspiderItem(Item):
    # define the fields for your item here like:
    name = Field()
    packageName = Field()
    version = Field()
    category = Field()
    size = Field()
    lastUpdated = Field()
    tags = Field()
