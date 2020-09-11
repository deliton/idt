import argparse
import os
import time
import re
import requests
import random
from PIL import Image
from io import BytesIO
from click import progressbar
from flickrapi import FlickrAPI

# Flickr API key https://www.flickr.com/services/apps/create/apply
__key__ = '6599353e91380cdb10e171956265aa73'
__secret__ = '267ea32c2539df88'

__name__ = "flickr"


class FlickrSearchEngine:
    def __init__(self,  data, n_images, folder, verbose, root_folder, size):
        self.data = data
        self.n_images = n_images
        self.folder = folder
        self.verbose = verbose
        self.root_folder = root_folder
        self.size = size
        self.downloaded_images = 0
        self.search()

    def search(self):
        t = time.time()
        flickr = FlickrAPI(__key__, __secret__)
        photos = flickr.walk(text=self.data,  # http://www.flickr.com/services/api/flickr.photos.search.html
                             extras='url_o',
                             per_page=100,
                             sort='relevance')

        urls = []
        page_counter = 0

        while page_counter < self.n_images:
            if self.n_images < 100:
                limit = self.n_images
            else:
                limit = 100

            print("\nDownloading {keyword} images page {page}...\n".format(
                keyword=self.data, page=int(page_counter/100)))

            page_counter += 100

            if not os.path.exists(self.root_folder):
                os.mkdir(self.root_folder)

            target_folder = os.path.join(self.root_folder, self.folder)
            if not os.path.exists(target_folder):
                os.mkdir(target_folder)

            with progressbar(length=self.n_images,
                             label='Downloading {keyword}'.format(keyword=self.data)) as progress_bar:
                for num, photo in enumerate(photos):
                    if num == self.n_images:
                        break
                    try:
                        # self.download(link, num)
                        url = photo.get('url_o')
                        if url is None:
                            url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % \
                                (photo.get('farm'), photo.get('server'), photo.get(
                                    'id'), photo.get('secret'))  # large size

                        self.download(url, num)
                        progress_bar.update(self.downloaded_images)
                        downloaded_images += 1
                        urls.append(url)
                    except:
                        continue

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
            img_name = folder

        if img_type.lower() != "jpg":
            raise Exception("Cannot download these type of file")
        else:
            # Check if another file of the same name already exists
            if os.path.exists("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder, className=self.folder, image_name=img_name, i=counter)):
                img.save("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder,
                                                                                       className=self.folder, image_name=img_name, i=random.randrange(1000000)), "JPEG")
            else:
                img.save("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(
                    root_folder=self.root_folder, className=self.folder, image_name=img_name, i=counter), "JPEG")
            self.downloaded_images += 1
