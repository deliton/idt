import os
import json 
import requests # to sent GET requests
import re
from PIL import Image
from io import BytesIO
from click import progressbar, echo

# user can input a topic and a number
# download first n images from google image search

__name__ = "bing"

class BingSearchEngine:
	def __init__(self,data,n_images,folder,verbose,root_folder,size):
		self.data = data
		self.n_images = n_images
		self.folder = folder
		self.verbose = verbose
		self.root_folder = root_folder
		self.size = size
		self.search()

	def search(self):
		BING_IMAGE = 'https://www.bing.com/images/async?q='

		USER_AGENT = {
	    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
	    }

		data = self.data.replace(" ", "-")

		if data[0] == "-":
			data  = data[1:]

		start_index = 0
		page_counter = 0

		while page_counter < self.n_images:
			if self.n_images < 100:
				limit = self.n_images
			else:
				limit = 100

			searchurl = BING_IMAGE + data + '&first=' + str(page_counter) + '&count=' + str(limit)

		    # request url, without usr_agent the permission gets denied
			response = requests.get(searchurl, headers=USER_AGENT)
			html = response.text
			page_counter += 100

			results = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

			print("\nDownloading {keyword} images page {page}...\n".format(keyword=data, page=int(page_counter/100)))

			if not os.path.exists(self.root_folder):
				os.mkdir(self.root_folder)

			target_folder = os.path.join(self.root_folder, self.folder)
			if not os.path.exists(target_folder):
				os.mkdir(target_folder)

			with progressbar(enumerate(results),
		                       length=len(results)) as results_enumerated:
				for num, link in results_enumerated:
					try:
						self.download(link, num)
						downloaded_images += 1
					except:
						continue
				
		    
		print('\nDone\n')

	def download(self, link, counter):
		IMG_SIZE = self.size, self.size
		response = requests.get(link, timeout=3.000)
		file = BytesIO(response.content)
		img = Image.open(file)
		img.thumbnail(IMG_SIZE, Image.ANTIALIAS)

	    # Split last part of url to get image name
		img_name = link.rsplit('/', 1)[1]
		img_type = img_name.split('.')[1]
		img_name = img_name.split('.')[0]

		# No every link ends like this, so use the class name when it doesn't apply
		if img_name == "":
			img_name = self.folder

		if img_type.lower() != "jpg":
			raise Exception("Cannot download these type of file")
		else:
			#Check if another file of the same name already exists
			if os.path.exists("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder,className=self.folder,image_name=img_name, i=counter)):
				img.save("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder,className=self.folder, image_name=img_name, i=random.randrange(1000000)), "JPEG")
			else:
				img.save("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder,className=self.folder, image_name=img_name, i=counter), "JPEG")