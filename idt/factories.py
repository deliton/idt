from idt.duckgo import DuckGoSearchEngine
from idt.bing import BingSearchEngine
from idt.bing_api import BingApiSearchEngine 
from idt.flickr_api import FlickrApiSearchEngine

__name__ = "factories"

class SearchEngineFactory:
	def __init__(self,data,n_images,folder,resize_method,root_folder,size,engine,api_key):
		self.data = data
		self.n_images = n_images
		self.folder = folder
		self.resize_method = resize_method
		self.root_folder = root_folder
		self.size = size
		self.engine = engine
		self.api_key = api_key
		self.getSearchEngine() 

	def getSearchEngine(self):
		if self.engine == "duckgo":
			return DuckGoSearchEngine(self.data, self.n_images, self.folder,self.resize_method,self.root_folder, self.size)
		elif self.engine == "bing":
			return BingSearchEngine(self.data, self.n_images, self.folder, self.resize_method, self.root_folder, self.size)
		elif self.engine == "bing_api":
			return BingApiSearchEngine(self.data, self.n_images, self.folder, self.resize_method, self.root_folder, self.size, self.api_key)
		elif self.engine == "flickr_api":
			return FlickrApiSearchEngine(self.data, self.n_images, self.folder, self.resize_method, self.root_folder, self.size, self.api_key)
		else:
			return None
