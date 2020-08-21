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
    
def bingImagesScraper(data,n_images,folder,verbose,root_folder):

	BING_IMAGE = \
    'https://www.bing.com/images/async?q='

	usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }
   

	data = data.replace(" ", "-")
	if data[0] == "-":
		data  = data[1:]

	start_index = 0
	page_counter = 0
	downloaded_images = 0
    
    # get url query string
	searchurl = BING_IMAGE + data + '&first=' + str(page_counter) + '&count=' + str(n_images)
	#print(searchurl)

    # request url, without usr_agent the permission gets denied
	response = requests.get(searchurl, headers=usr_agent)
	html = response.text

    # find all divs where class='rg_meta'
	results = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

	print("Downloading {keyword} images...\n".format(keyword=data))

	if not os.path.exists(root_folder):
		os.mkdir(root_folder)

	target_folder = os.path.join(root_folder, folder)
	if not os.path.exists(target_folder):
		os.mkdir(target_folder)

	with progressbar(enumerate(results),
                       length=len(results)) as results_enumerated:
		for num, link in results_enumerated:
			try:
				download(link, folder, 512, num,root_folder)
			except:
				#echo("Failed to download {link}".format(link=link))
				continue
		

    
    # extract the link from the div tag
	print('\nDone\n')


def download(link, folder, size, counter, root_folder ):

	IMG_SIZE = size, size
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
		img_name = folder

	if img_type.lower() != "jpg":
		raise Exception("Cannot download these type of file")
	else:
		#Check if another file of the same name already exists
		if os.path.exists("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=root_folder,className=folder,image_name=img_name, i=counter)):
			img.save("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=root_folder,className=folder, image_name=img_name, i=random.randrange(1000000)), "JPEG")
		else:
			img.save("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=root_folder,className=folder, image_name=img_name, i=counter), "JPEG")
	                


