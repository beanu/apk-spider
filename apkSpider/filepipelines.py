from twisted.internet import defer, threads

from scrapy.selector import HtmlXPathSelector
from scrapy.shell import inspect_response

from scrapy.xlib.pydispatch import dispatcher
from scrapy import log
from scrapy.http import Request
from scrapy.exceptions import DropItem, NotConfigured, IgnoreRequest
from scrapy.contrib.pipeline.media import MediaPipeline

from collections import defaultdict
import re
import os

class FileException(Exception):
	"""General file error exception"""

class APKFilePipeline(MediaPipeline):
	MEDIA_NAME = 'apkfile'
	def __init__(self, store_uri, download_func=None):
		self.created_directories = defaultdict(set)
		self.basedir = store_uri
		self._mkdir(self.basedir)
		
		super(APKFilePipeline, self).__init__(download_func=download_func)

	@classmethod
	def from_settings(cls, settings):
		store_uri = settings['APKFILES_STORE']
		return cls(store_uri)


	def media_downloaded(self, response, request, info):
		log.msg('-----Downloading+++++')
		referer = request.headers.get('Referer')
		if response.status != 200:
			log.msg('File (code: %s): Error downloading file from %s referred in <%s>' \
                    % (response.status, request, referer), level=log.WARNING, spider=info.spider)
			raise FileException
		if not response.body:
			log.msg('File (empty-content): Empty file from %s referred in <%s>: no-content' \
                    % (request, referer), level=log.WARNING, spider=info.spider)
			raise FileException
	
		p=re.compile(r'filename=\S+\.((\w|\d)+)')
		header=  response.headers['Content-Disposition'];
		header = ''.join(header)
		suffix="";
		match = p.search(header)
		if match:
			suffix=match.group(1)
		packageName = response.meta['packageName']
		filename = self.gen_filename(packageName,suffix)

		absolute_path = self._get_filesystem_path(filename)
		self._mkdir(os.path.dirname(absolute_path))
		file = open(absolute_path,"wb")
		file.write(response.body)
		file.close
#		inspect_response(response)
		return {'url': request.url, 'path': filename}

	def gen_filename(self, packageName,suffix):
		# file_guid = hashlib.sha1(url).hexdigest()
		_path=packageName.split('.')[-1].lower()
		_pathA="a"
		_pathB="b"
		if len(_path)>=2:
			_pathA=_path[0]
			_pathB=_path[1]
		elif len(_path)==1:
			_pathA=_path[0]
			_pathB=_path[0]
		return '%s/%s/%s.%s' % (_pathA,_pathB,packageName,suffix);
		

	def _get_filesystem_path(self, key):
		path_comps = key.split('/')
		return os.path.join(self.basedir, *path_comps)

	def _mkdir(self, dirname, domain=None):
		seen = self.created_directories[domain] if domain else set()
		if dirname not in seen:
			if not os.path.exists(dirname):
				os.makedirs(dirname)
			seen.add(dirname)

	def get_media_requests(self, item, info):
		if item['downloadUrl']:
			log.msg('-----Request+++++')
			req = Request(url=item['downloadUrl'][0])
			req.meta['packageName']=item['packageName']
			return [req]
			#yield Request(link)
		return;

	def item_completed(self, results, item, info):
		for ok,x in results:
			if ok:
				item["apkPath"]=x['path']
		return item;