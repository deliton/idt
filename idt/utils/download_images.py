import uuid
import requests;
import os;
from PIL import Image
from io import BytesIO

__name__ = "download_images"

def download(link, counter, size, root_folder, class_name):
    IMG_SIZE = size, size
    response = requests.get(link, timeout=3.000)
    file = BytesIO(response.content)
    img = Image.open(file)
    if size > 0:
        IMG_SIZE = size, size
        img.thumbnail(IMG_SIZE, Image.ANTIALIAS)

    # Split last part of url to get image name
    img_name = link.rsplit('/', 1)[1]
    img_type = img_name.split('.')[1]

    if img_type.lower() != "jpg":
        raise Exception("Cannot download these type of file")
    else:
        #Check if another file of the same name already exists
        id = uuid.uuid1() 
        img.save(f"./{root_folder}/{class_name}/{class_name}-{id.hex}.jpg", "JPEG")