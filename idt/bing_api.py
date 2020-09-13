import os
import json 
import requests
import re

from idt.utils.download_images import download
from idt.utils.create_dataset_csv import generate_class_info
from rich.progress import Progress

__name__ = "bing_api"

class BingApiSearchEngine:
	def __init__(self,data,n_images,folder,verbose,root_folder,size,api_key):
		self.data = data
		self.n_images = n_images
		self.folder = folder
		self.verbose = verbose
		self.root_folder = root_folder
		self.size = size
		self.downloaded_images = 0
		self.dataset_info = []
		self.page = 0
		self.api_key = api_key
		self.search()

	def search(self):
		BING_IMAGE = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'

		headers = {"Ocp-Apim-Subscription-Key" : self.api_key}
		params  = {"q": self.data, "count": 100, "offset": self.page}

		page_counter = 0
		with Progress() as progress:
			task1 = progress.add_task(f"Downloading [blue]{self.data}[/blue] class...",total=self.n_images)
			while self.downloaded_images < self.n_images:
				response = requests.get(BING_IMAGE, headers=headers, params=params)
				response.raise_for_status()
				results = response.json()
				self.page += 100

				if not os.path.exists(self.root_folder):
					os.mkdir(self.root_folder)

				target_folder = os.path.join(self.root_folder, self.folder)
				if not os.path.exists(target_folder):
					os.mkdir(target_folder)

				for num, result in enumerate(results['value']):
					try:
						if self.downloaded_images < self.n_images:
							download(result['contentUrl'], num,self.size,self.root_folder,self.folder)
							self.dataset_info.append({
								'name': result['name'],
								'origin': result['hostPageDisplayUrl'].split('/')[2],
								'date': result['datePublished'],
								'original_size': result['contentSize'],
								'original_width': result['width'],
								'original_height' : result['height']})

							self.downloaded_images += 1
							progress.update(task1, advance=1)
						else:
							break; 
					except:
						continue
		generate_class_info(self.dataset_info,self.root_folder, self.folder)
