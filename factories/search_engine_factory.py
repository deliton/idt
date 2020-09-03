from crawlers.duckgo import DuckGoSearchEngine
from crawlers.bing import BingSearchEngine
from crawlers.deviantart import DeviantArtSearchEngine
from crawlers.pinterest import PinterestSearchEngine

__name__ = "engine_factory"

class SearchEngineFactory:
	def __init__(self,data,n_images,folder,verbose,root_folder,size,engine):
		self.data = data
		self.n_images = n_images
		self.folder = folder
		self.verbose = verbose
		self.root_folder = root_folder
		self.size = size
		self.engine = engine
		self.getSearchEngine() 

	def getSearchEngine(self):
		if self.engine == "duckgo":
			return DuckGoSearchEngine(self.data, self.n_images, self.folder,self.verbose,self.root_folder, self.size)
		elif self.engine == "bing":
			return BingSearchEngine(self.data, self.n_images, self.folder,self.verbose,self.root_folder, self.size)
		elif self.engine == "deviantart":
			return DeviantArtSearchEngine(self.data, self.n_images, self.folder,self.verbose,self.root_folder, self.size)
		elif self.engine == "pinterest":
			return PinterestSearchEngine(self.data, self.n_images, self.folder,self.verbose,self.root_folder, self.size)
		elif self.engine == "google_images":
			return None
		else:
			return None
