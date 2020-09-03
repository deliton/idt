import os
import json 
import requests
import re
from PIL import Image
from io import BytesIO
from click import progressbar, echo
import random

__name__ = "deviantart"

class DeviantArtSearchEngine:
	def __init__(self,data,n_images,folder,verbose,root_folder,size):
		self.data = data
		self.n_images = n_images
		self.folder = folder
		self.verbose = verbose
		self.root_folder = root_folder
		self.size = size
		self.downloaded_images = 0
		self.search()
		
	def search(self):
		DEVIANTART_LINK = 'https://www.deviantart.com/search/deviations'

		USER_AGENT = {
	    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
	    }

		page_counter = 0
		index_counter = 0

		while index_counter < self.n_images:

			searchurl = DEVIANTART_LINK + '?page='+ str(page_counter) + '&q=' + self.data

		    # request url, without usr_agent the permission gets denied
			response = requests.get(searchurl, headers=USER_AGENT)
			html = response.text
			page_counter += 1
			index_counter +=24

			results = re.findall('(https://images.*?jpg.*?)(?=. style)', html)

			print("\nDownloading {keyword} images page {page}...\n".format(keyword=self.data, page=page_counter))

			if not os.path.exists(self.root_folder):
				os.mkdir(self.root_folder)

			target_folder = os.path.join(self.root_folder, self.folder)
			if not os.path.exists(target_folder):
				os.mkdir(target_folder)

			if not results:
				return 0

			with progressbar(enumerate(results),
		                       length=len(results)) as results_enumerated:
				for num, link in results_enumerated:
					try:
						if self.downloaded_images < self.n_images:
							self.download(link, num)
							#print("LINK" , link)
							self.downloaded_images+=1
						else:
							return 0

					except Exception as e:
						continue
				
		    
		print('\nDone\n')

	def download(self, link, counter):
		IMG_SIZE = self.size, self.size
		response = requests.get(link, timeout=3.000)
		file = BytesIO(response.content)
		img = Image.open(file)
		img.thumbnail(IMG_SIZE, Image.ANTIALIAS)

		#Check if another file of the same name already exists
		if os.path.exists("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder,className=self.folder,image_name=self.folder, i=counter)):
			img.save("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder,className=self.folder, image_name=self.folder, i=random.randrange(1000000)), "JPEG")
		else:
			img.save("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder,className=self.folder, image_name=self.folder, i=counter), "JPEG")
		self.downloaded_images += 1