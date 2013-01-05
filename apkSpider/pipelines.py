# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem

class ApkPipeline(object):
    def __init__(self):
        connection=pymongo.Connection('localhost',27017)
        db=connection['test']
        self.collection=db['scrapy']

    def process_item(self, item, spider):
        vaild=True
        for data in item:
            if not data:
                vaild=False
                raise DropItem("Missing %s of data from %s" %(data,item['name']))
        if vaild:
            self.collection.insert(dict(item))
        return item
