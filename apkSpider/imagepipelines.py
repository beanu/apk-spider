from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

#Image
class MyImagesPipeline(ImagesPipeline):
    # def media_downloaded(self, response, request, info):
    #     referer = request.headers.get('Referer')

    #     if response.status != 200:
    #         log.msg(format='Image (code: %(status)s): Error downloading image from %(request)s referred in <%(referer)s>',
    #                 level=log.WARNING, spider=info.spider,
    #                 status=response.status, request=request, referer=referer)
    #         raise ImageException('download-error')

    #     if not response.body:
    #         log.msg(format='Image (empty-content): Empty image from %(request)s referred in <%(referer)s>: no-content',
    #                 level=log.WARNING, spider=info.spider,
    #                 request=request, referer=referer)
    #         raise ImageException('empty-content')

    #     status = 'cached' if 'cached' in response.flags else 'downloaded'
    #     log.msg(format='Image (%(status)s): Downloaded image from %(request)s referred in <%(referer)s>',
    #             level=log.DEBUG, spider=info.spider,
    #             status=status, request=request, referer=referer)
    #     self.inc_stats(info.spider, status)

    #     try:
    #         key = self.image_key(request.url,request.meta.get('path'))
    #         checksum = self.image_downloaded(response, request, info)
    #     except ImageException as exc:
    #         whyfmt = 'Image (error): Error processing image from %(request)s referred in <%(referer)s>: %(errormsg)s'
    #         log.msg(format=whyfmt, level=log.WARNING, spider=info.spider,
    #                 request=request, referer=referer, errormsg=str(exc))
    #         raise
    #     except Exception as exc:
    #         whyfmt = 'Image (unknown-error): Error processing image from %(request)s referred in <%(referer)s>'
    #         log.err(None, whyfmt % {'request': request, 'referer': referer}, spider=info.spider)
    #         raise ImageException(str(exc))

    #     return {'url': request.url, 'path': key, 'checksum': checksum}

    # def media_to_download(self, request, info):
    #     def _onsuccess(result):
    #         if not result:
    #             return  # returning None force download

    #         last_modified = result.get('last_modified', None)
    #         if not last_modified:
    #             return  # returning None force download

    #         age_seconds = time.time() - last_modified
    #         age_days = age_seconds / 60 / 60 / 24
    #         if age_days > self.EXPIRES:
    #             return  # returning None force download

    #         referer = request.headers.get('Referer')
    #         log.msg(format='Image (uptodate): Downloaded %(medianame)s from %(request)s referred in <%(referer)s>',
    #                 level=log.DEBUG, spider=info.spider,
    #                 medianame=self.MEDIA_NAME, request=request, referer=referer)
    #         self.inc_stats(info.spider, 'uptodate')

    #         checksum = result.get('checksum', None)
    #         return {'url': request.url, 'path': key, 'checksum': checksum}

    #     key = self.image_key(request.url,request.meta.get('path'))
    #     dfd = defer.maybeDeferred(self.store.stat_image, key, info)
    #     dfd.addCallbacks(_onsuccess, lambda _: None)
    #     dfd.addErrback(log.err, self.__class__.__name__ + '.store.stat_image')
    #     return dfd

    # def get_images(self, response, request, info):
    #     key = self.image_key(request.url,request.meta.get('path'))
    #     orig_image = Image.open(StringIO(response.body))

    #     width, height = orig_image.size
    #     if width < self.MIN_WIDTH or height < self.MIN_HEIGHT:
    #         raise ImageException("Image too small (%dx%d < %dx%d)" %
    #                              (width, height, self.MIN_WIDTH, self.MIN_HEIGHT))

    #     image, buf = self.convert_image(orig_image)
    #     yield key, image, buf

    #     for thumb_id, size in self.THUMBS.iteritems():
    #         thumb_key = self.thumb_key(request.url, thumb_id)
    #         thumb_image, thumb_buf = self.convert_image(image, size)
    #         yield thumb_key, thumb_image, thumb_buf

    # def image_key(self, url, path):
    #     image_guid = hashlib.sha1(url).hexdigest()
    #     return 'full/%s/%s.jpg' % (path,image_guid)

    def get_media_requests(self, item, info):
        for image_url in item['screenshot']:
            yield Request(url=image_url,meta={"path":item['packageName']})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['screenshotPath'] = image_paths
        return item