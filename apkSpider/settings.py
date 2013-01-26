# Scrapy settings for apkSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'apkSpider'

SPIDER_MODULES = ['apkSpider.spiders']
NEWSPIDER_MODULE = 'apkSpider.spiders'

ITEM_PIPELINES = ['apkSpider.imagepipelines.MyImagesPipeline','apkSpider.filepipelines.APKFilePipeline','apkSpider.pipelines.StoreDataPipeline']
DOWNLOADER_MIDDLEWARES = {'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,'apkSpider.middlewares.ProxyMiddleware': 100,}

DOWNLOAD_DELAY = 0.25

APKFILES_STORE = '/home/beanu/tmp'
IMAGES_STORE = '/home/beanu/tmp'
IMAGES_EXPIRES = 90

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'apkSpider (+http://www.yourdomain.com)'