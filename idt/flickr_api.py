import os
import json 
import requests
import re

from idt.utils.download_images import download
from idt.utils.remove_corrupt import erase_duplicates
from rich.progress import Progress

__name__ = "flickr_api"

class FlickrApiSearchEngine:
	def __init__(self,data,n_images,folder,resize_method,root_folder,size,api_key):
		self.data = data
		self.n_images = n_images
		self.folder = folder
		self.resize_method = resize_method
		self.root_folder = root_folder
		self.size = size
		self.downloaded_images = 0
		self.dataset_info = []
		self.page = 1
		self.api_key = api_key
		self.search()

	def search(self):
		FLICKR_LINK = 'https://www.flickr.com/services/rest/'

		#headers = {"Ocp-Apim-Subscription-Key" : self.api_key}
		data = self.data.replace(" ", "+")

		if data[0] == "+":
			data  = data[1:]

		params = {
		"method": "flickr.photos.search",
		"api_key": self.api_key,
		"tags": data,
		"format": "json",
		"page": self.page,
		"nojsoncallback": 1
		}
		with Progress() as progress:
			task1 = progress.add_task(f"Downloading [blue]{self.data}[/blue] class...",total=self.n_images)
			while self.downloaded_images < self.n_images:
				response = requests.get(FLICKR_LINK, params=params)
				response.raise_for_status()
				results = response.json()
				results = results['photos']
				if results['total'] == 0:
					progress.update(task1, advance=self.n_images)
					return 0
				
				self.page += 1

				if not os.path.exists(self.root_folder):
					os.mkdir(self.root_folder)

				target_folder = os.path.join(self.root_folder, self.folder)
				if not os.path.exists(target_folder):
					os.mkdir(target_folder)

				for result in results['photo']:
					try:
						if self.downloaded_images < self.n_images:
							link = f"https://farm{result['farm']}.staticflickr.com/{result['server']}/{result['id']}_{result['secret']}.jpg"
							download(link, self.size,self.root_folder,self.folder, self.resize_method)
							self.downloaded_images += 1
							progress.update(task1, advance=1)
						else:
							break; 
					except:
						continue
				self.downloaded_images -= erase_duplicates(target_folder)
