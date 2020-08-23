import requests;
import re;
import json;
import time;
import logging;
import os;
from PIL import Image
from io import BytesIO
import random
from click import progressbar

__name__ = "duckgo"

class DuckGoSearchEngine:
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
        URL = 'https://duckduckgo.com/'
        PARAMS = {'q': self.data}
        HEADERS = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,en;q=0.9'}

        res = requests.post(URL, data=PARAMS, timeout=3.000)
        search_object = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I)
        #print(search_object)

        if not search_object:
            return -1;

        PARAMS = (
        ('l', 'us-en'),
        ('o', 'json'),
        ('q', self.data),
        ('vqd', search_object.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'))

        request_url = URL + "i.js";
        with progressbar(length=self.n_images,
                       label='Downloading {keyword}'.format(keyword=self.data)) as progress_bar:
            while self.downloaded_images < self.n_images:
                while True:
                    try:
                        res = requests.get(request_url, headers=HEADERS, params=PARAMS, timeout=3.000);
                        data = json.loads(res.text);
                        break;
                    except ValueError as e:
                        time.sleep(5);
                        continue;

                if not os.path.exists(self.root_folder):
                    os.mkdir(self.root_folder)

                target_folder = os.path.join(self.root_folder, self.folder)
                if not os.path.exists(target_folder):
                    os.mkdir(target_folder)

                # Cut the extra result by the amount that still need to be downloaded
                if len(data["results"]) > self.n_images - self.downloaded_images:
                    data["results"] = data["results"][:self.n_images - self.downloaded_images]

                for num, results in enumerate(data["results"]):
                    try:
                        self.download(results["image"], num)
                        progress_bar.update(self.downloaded_images)
                        
                    except Exception as e:
                        continue

                if "next" not in data:
                    return 0

                request_url = URL + data["next"];

    def download(self,link, counter):
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
            #Check if another file of the same name already exists
            if os.path.exists("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder,className=self.folder,image_name=img_name, i=counter)):
                img.save("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder,className=self.folder, image_name=img_name, i=random.randrange(1000000)), "JPEG")
            else:
                img.save("./{root_folder}/{className}/idb-{image_name}-{i}.jpg".format(root_folder=self.root_folder,className=self.folder, image_name=img_name, i=counter), "JPEG")
            self.downloaded_images+= 1