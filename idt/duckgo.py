import requests;
import re;
import json;
import time;
import logging;
import os;
from rich.progress import Progress

from idt.utils.download_images import download
from idt.utils.remove_corrupt import erase_duplicates

__name__ = "duckgo"

class DuckGoSearchEngine:
    def __init__(self,  data, n_images, folder, resize_method, root_folder, size):
        self.data = data
        self.n_images = n_images
        self.folder = folder
        self.resize_method = resize_method
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
        with Progress() as progress:

            task1 = progress.add_task("[blue]Downloading {x} class...".format(x=self.data), total=self.n_images)
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

                for results in data["results"]:
                    try:
                        download(results["image"], self.size, self.root_folder, self.folder, self.resize_method)
                        self.downloaded_images+= 1
                        progress.update(task1, advance=1) 
                    except Exception as e:
                        continue
                        
                self.downloaded_images -= erase_duplicates(target_folder)

                if "next" not in data:
                    return 0
                request_url = URL + data["next"];
