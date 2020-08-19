import requests;
import re;
import json;
import time;
import logging;
import os;
from PIL import Image
from io import BytesIO
import random
import sys

__name__ = "duckgo"


def duckgoSearch(keywords, max_results,verbose):
    url = 'https://duckduckgo.com/';
    params = {
        'q': keywords
    };

    #logging.basicConfig(level=logging.DEBUG);
    logger = logging.getLogger(__name__)
    logger.disabled = verbose
    logger.debug("Hitting DuckDuckGo for Token");
    print("\n")

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params, timeout=3.000)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I);

    if not searchObj:
        logger.error("Token Parsing Failed !");
        return -1;

    logger.debug("Obtained Token");

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('l', 'us-en'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    requestUrl = url + "i.js";

    logger.debug("Hitting Url : %s", requestUrl);

    while True:
        while True:
            try:
                res = requests.get(requestUrl, headers=headers, params=params, timeout=3.000);
                data = json.loads(res.text);
                break;
            except ValueError as e:
                logger.debug("Hitting Url Failure - Sleep and Retry: %s", requestUrl);
                time.sleep(5);
                continue;

        logger.debug("Hitting Url Success : %s", requestUrl);

        saveResults(data["results"],keywords,max_results, verbose);

        if "next" not in data:
            logger.debug("No Next Page - Exiting");
            exit(0);

        requestUrl = url + data["next"];

# ISSUE: reimplement this method in order to make ir more general purpose and work on other search engines
def saveResults(objs, className,max_results,verbose):

    if os.path.exists(className):
        dir = os.path.dirname(className)
    else:
        dir = os.mkdir(className)

    size = 512, 512
    i = 1

    for idx, obj in enumerate(objs):
        
        show(idx, 100, "Building {className} dataset: ".format(className=className),max_results,sys.stdout)

        # ISSUE: find a better way to stop search when index reaches max value
        if idx == max_results:
            print("\n")
            exit(0)

        try:
            # Raise exception if requests is unable to reach target
            response = requests.get(obj["image"], timeout=3.000)
            try:
                # ISSUE: find a way to filter the corrupt images
                # Raise exception if file cannot create a thumbnail
                file = BytesIO(response.content)
                img = Image.open(file)
                img.thumbnail(size, Image.ANTIALIAS)

                # Split last part of url to get image name
                img_name = obj["url"].rsplit('/', 1)[1]

                # No every link ends like this, so use the class name when it doesn't apply
                if img_name == "":
                    img_name = className

                #Check if another file of the same name already exists
                if os.path.exists("./{className}/idb-{image_name}-{i}".format(className=className,image_name=img_name, i=idx)):
                    img.save("./{className}/idb-{image_name}-{i}".format(className=className, image_name=img_name, i=random.randrange(1000000)), "JPEG")
                else:
                    img.save("./{className}/idb-{image_name}-{i}".format(className=className, image_name=img_name, i=idx), "JPEG")
                
            except:
                if verbose:
                    print("Invalid file. ignoring image")
                continue
        except:
            if verbose:
                print("cannot load this request. skipping to the next path")
            continue

# Show progress bar
# ISSUE: move this method to the analyzers module in order to make this more general purpose
# ISSUE: find a way to fix the progress bar when verbose is on or more things need to be printed
def show(j, size, prefix, count, file):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        #file.flush() 
