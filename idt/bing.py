import os
import json 
import requests
import re

from idt.utils.download_images import download
from idt.utils.remove_corrupt import erase_duplicates

from rich.progress import Progress

__name__ = "bing"

class BingSearchEngine:
	def __init__(self,data,n_images,folder,verbose,root_folder,size):
		self.data = data
		self.n_images = n_images
		self.folder = folder
		self.verbose = verbose
		self.root_folder = root_folder
		self.size = size
		self.downloaded_images = 0
		self.page = 0
		self.search()

	def search(self):
		BING_IMAGE = 'https://www.bing.com/images/async?q='

		USER_AGENT = {
		'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}

		data = self.data.replace(" ", "-")

		if data[0] == "-":
			data  = data[1:]

		page_counter = 0
		with Progress() as progress:
			task1 = progress.add_task(f"Downloading [blue]{self.data}[/blue] class...",total=self.n_images)
			while self.downloaded_images < self.n_images:
				searchurl = BING_IMAGE + data + '&first=' + str(self.page) + '&count=100'

			    # request url, without usr_agent the permission gets denied
				response = requests.get(searchurl, headers=USER_AGENT)
				html = response.text
				self.page += 100
				results = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

				if not os.path.exists(self.root_folder):
					os.mkdir(self.root_folder)

				target_folder = os.path.join(self.root_folder, self.folder)
				if not os.path.exists(target_folder):
					os.mkdir(target_folder)

				for num, link in enumerate(results):
					try:
						if self.downloaded_images < self.n_images:
							download(link, num,self.size,self.root_folder,self.folder)
							self.downloaded_images += 1
							progress.update(task1, advance=1)
						else:
							break; 
					except:
						continue
				self.downloaded_images -= erase_duplicates(target_folder)
		print('Done')
