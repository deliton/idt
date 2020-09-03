import os
import json 
import requests
import re
from PIL import Image
from io import BytesIO
from click import progressbar, echo
import random

__name__ = "pinterest"

class PinterestSearchEngine:
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
		PINTEREST_LINK = 'https://www.pinterest.com/search/pins/'

		USER_AGENT = {
	    'authority': 'br.pinterest.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://br.pinterest.com/',
        'accept-language': 'en-US,en;q=0.9'
	    }

		page_counter = 0
		index_counter = 0

		while index_counter < self.n_images:

			searchurl = PINTEREST_LINK + '?q=' + self.data + '&rs=typed&term_meta[]={data}|typed'.format(data=self.data)

		    # request url, without usr_agent the permission gets denied
			response = requests.get(searchurl, headers=USER_AGENT)
			html = response.text
			page_counter += 1
			index_counter +=24

			print(html)

			results = re.findall('(?<=2x, )(.*?jpg.*?)(?= 3x)', html)
			print(results)

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
							#self.download(link, num)
							print("LINK" , link)
							self.downloaded_images+=1
						else:
							return 0

					except Exception as e:
						print(e)
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