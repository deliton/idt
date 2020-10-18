from PIL import Image

def crop_longer_side(img, size):
	IMG_SIZE = size, size
	img.thumbnail(IMG_SIZE, Image.ANTIALIAS)
	return img
